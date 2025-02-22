from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, FileResponse
import logging
import importlib.util
import sys
import os
from datetime import datetime

from .models import Workflow
from .forms import WorkflowForm, ScriptUploadForm

logger = logging.getLogger(__name__)


# Create your views here.
class WorkflowListView(ListView):
    model = Workflow
    template_name = "workflows/workflow_list.html"
    context_object_name = "workflows"

    def get_queryset(self):
        queryset = super().get_queryset()
        logger.info(f"WorkflowListView - Found {queryset.count()} workflows")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.info(f"WorkflowListView - Context: {context}")
        return context


class WorkflowCreateView(CreateView):
    model = Workflow
    template_name = "workflows/workflow_new.html"
    fields = ["name", "description", "data_source"]

    def get_success_url(self):
        return reverse_lazy("workflows:workflow_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"Created new workflow: {self.object}")
        return response


class WorkflowDetailView(DetailView):
    model = Workflow
    template_name = "workflows/workflow_detail.html"
    context_object_name = "workflow"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workflow_form"] = WorkflowForm(instance=self.object)
        context["script_form"] = ScriptUploadForm()

        # Add the latest generated file if it exists
        if hasattr(self.object, "latest_output_file"):
            context["output_file"] = self.object.latest_output_file

        return context

    def post(self, request, *args, **kwargs):
        workflow = self.get_object()
        form_type = request.POST.get("form_type")

        if form_type == "script":
            form = ScriptUploadForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    if workflow.script_file:
                        workflow.script_file.delete(save=False)
                    workflow.script_file = form.cleaned_data["script_file"]
                    workflow.save()
                    logger.info(f"Script file saved to: {workflow.script_file.path}")
                    messages.success(request, "Script uploaded successfully.")
                except Exception as e:
                    logger.error(f"Error saving script: {str(e)}")
                    messages.error(request, f"Error saving script: {str(e)}")
        else:
            # Handle workflow file uploads and script execution
            try:
                # Handle file uploads directly without form validation
                if "template_file" in request.FILES:
                    if workflow.template_file:
                        workflow.template_file.delete(save=False)
                    workflow.template_file = request.FILES["template_file"]
                    logger.info(f"Template file being uploaded: {request.FILES['template_file'].name}")

                if "data_file" in request.FILES:
                    if workflow.data_file:
                        workflow.data_file.delete(save=False)
                    workflow.data_file = request.FILES["data_file"]
                    logger.info(f"Data file being uploaded: {request.FILES['data_file'].name}")

                workflow.save()

                if "template_file" in request.FILES or "data_file" in request.FILES:
                    messages.success(request, "Files uploaded successfully.")

                # Run script if all files are present and no new files were just uploaded
                if (
                    workflow.template_file
                    and workflow.data_file
                    and workflow.script_file
                    and "template_file" not in request.FILES
                    and "data_file" not in request.FILES
                ):
                    try:
                        # Load the script dynamically
                        spec = importlib.util.spec_from_file_location("workflow_script", workflow.script_file.path)
                        module = importlib.util.module_from_spec(spec)
                        sys.modules["workflow_script"] = module
                        spec.loader.exec_module(module)

                        # Run the process function
                        result = module.process(
                            template_file=workflow.template_file.path, data_file=workflow.data_file.path
                        )

                        # Store the result path if it was successful
                        if result and "Output saved to:" in result:
                            output_path = result.split("Output saved to:")[1].strip()
                            workflow.latest_output_file = output_path
                            workflow.save()

                        logger.info(f"Workflow execution result: {result}")
                        messages.success(request, "Script executed successfully.")

                    except Exception as e:
                        logger.error(f"Error executing script: {str(e)}")
                        messages.error(request, f"Error executing script: {str(e)}")

            except Exception as e:
                logger.error(f"Error processing files: {str(e)}")
                messages.error(request, f"Error processing files: {str(e)}")

        return redirect(reverse("workflows:workflow_detail", kwargs={"pk": workflow.pk}))


class WorkflowDeleteView(DeleteView):
    model = Workflow
    template_name = "workflows/workflow_delete.html"
    success_url = reverse_lazy("workflows:workflow_list")


class WorkflowUpdateView(UpdateView):
    model = Workflow
    form_class = WorkflowForm
    template_name = "workflows/workflow_edit.html"

    def get_success_url(self):
        return reverse_lazy("workflows:workflow_detail", kwargs={"pk": self.object.pk})


def validate_files(request, pk):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        form_type = request.POST.get("form_type")

        if form_type == "script":
            form = ScriptUploadForm(request.POST, request.FILES)
            results = {
                "all_valid": form.is_valid(),
                "script": {
                    "valid": form.is_valid(),
                    "message": "Valid Python script" if form.is_valid() else form.errors["script_file"][0],
                },
            }
        else:
            form = WorkflowForm(request.POST, request.FILES)
            results = {
                "all_valid": form.is_valid(),
                "template": {
                    "valid": "template_file" not in form.errors,
                    "message": "Valid Excel template"
                    if "template_file" not in form.errors
                    else form.errors["template_file"][0],
                },
                "data": {
                    "valid": "data_file" not in form.errors,
                    "message": "Valid data file" if "data_file" not in form.errors else form.errors["data_file"][0],
                },
            }

        return JsonResponse(results)
    except Exception as e:
        logger.error(f"Error validating files: {str(e)}")
        return JsonResponse({"error": str(e)}, status=400)


def download_script(request, workflow_id):
    workflow = get_object_or_404(Workflow, id=workflow_id)
    file_type = request.GET.get("type", "script")

    if file_type == "output" and workflow.template_file:
        try:
            # Debug logging
            logger.info(f"Starting download process for workflow {workflow_id}")
            logger.info(f"Template file exists: {os.path.exists(workflow.template_file.path)}")
            logger.info(f"Template file path: {workflow.template_file.path}")
            logger.info(f"Template file name: {workflow.template_file.name}")

            if not os.path.exists(workflow.template_file.path):
                raise FileNotFoundError(f"Template file not found at {workflow.template_file.path}")

            # Read file in binary mode
            with open(workflow.template_file.path, "rb") as excel_file:
                file_content = excel_file.read()

            if not file_content:
                raise ValueError("File content is empty")

            response = HttpResponse(
                file_content,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

            # Create filename
            base_name = os.path.splitext(os.path.basename(workflow.template_file.name))[0]
            filename = f"{base_name}_{datetime.now().strftime('%Y%m%d')}.xlsx"

            logger.info(f"Preparing download with filename: {filename}")

            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            response["Content-Length"] = len(file_content)

            return response

        except Exception as e:
            logger.error(f"Error downloading template file: {str(e)}", exc_info=True)
            messages.error(request, f"Error downloading template file: {str(e)}")
    elif workflow.script_file:
        return FileResponse(workflow.script_file.open(), as_attachment=True)
    else:
        messages.error(request, "No file found")

    return redirect("workflows:workflow_detail", pk=workflow_id)
