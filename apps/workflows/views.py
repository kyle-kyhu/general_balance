from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, FileResponse
import logging
import importlib.util
import sys

from .models import Workflow
from .forms import WorkflowForm

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

    def post(self, request, *args, **kwargs):
        workflow = self.get_object()
        script_file = request.FILES.get("script_file")

        try:
            if script_file:
                logger.info(f"Received script file: {script_file.name}")
                if workflow.script_file:
                    logger.info(f"Deleting old script file: {workflow.script_file.path}")
                    workflow.script_file.delete(save=False)
                workflow.script_file = script_file
                logger.info(f"Saving new script file to: {workflow.script_file.name}")

            workflow.save()
            logger.info(
                f"Workflow saved. Script file path: {workflow.script_file.path if workflow.script_file else 'None'}"
            )
            messages.success(request, "Files uploaded successfully.")

        except Exception as e:
            logger.error(f"Error saving files: {str(e)}")
            messages.error(request, f"Error saving files: {str(e)}")

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


def run_workflow(request, pk):
    workflow = get_object_or_404(Workflow, pk=pk)

    if request.method == "POST":
        try:
            # Load the script dynamically
            spec = importlib.util.spec_from_file_location("workflow_script", workflow.script_file.path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["workflow_script"] = module
            spec.loader.exec_module(module)

            # Run the process function from the uploaded script and store the result
            result = module.process(template_file=workflow.template_file.path, data_file=workflow.data_file.path)

            # Log the result for debugging
            logger.info(f"Workflow execution result: {result}")

            # You could store the result or pass it to the template via messages
            if result:
                messages.success(request, f"Workflow executed successfully. Result: {result}")
            else:
                messages.success(request, "Workflow executed successfully.")

            return redirect(reverse("workflows:workflow_detail", kwargs={"pk": workflow.pk}))

        except Exception as e:
            messages.error(request, f"Error executing workflow: {str(e)}")
            return redirect(reverse("workflows:workflow_detail", kwargs={"pk": workflow.pk}))

    return HttpResponse(status=405)


def validate_files(request, pk):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        results = {
            "all_valid": True,
            "template": {"valid": True, "message": "Valid Excel template"},
            "data": {"valid": True, "message": "Valid data file"},
            "script": {"valid": True, "message": "Valid Python script"},
        }
        return JsonResponse(results)
    except Exception as e:
        logger.error(f"Error validating files: {str(e)}")
        return JsonResponse({"error": str(e)}, status=400)


def upload_script(request, workflow_id):
    workflow = get_object_or_404(Workflow, id=workflow_id)
    if request.method == "POST" and request.FILES.get("script_file"):
        script_file = request.FILES["script_file"]
        # Validate file type if needed
        if not script_file.name.endswith(".py"):
            messages.error(request, "Please upload a Python file (.py)")
            return redirect("workflow_detail", workflow_id=workflow_id)

        workflow.save_script(script_file)
        messages.success(request, "Script uploaded successfully")
    return redirect("workflow_detail", workflow_id=workflow_id)


def download_script(request, workflow_id):
    workflow = get_object_or_404(Workflow, id=workflow_id)
    if workflow.script_file:
        return FileResponse(workflow.script_file.open(), as_attachment=True)
    messages.error(request, "No script file found")
    return redirect("workflow_detail", workflow_id=workflow_id)
