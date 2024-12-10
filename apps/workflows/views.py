from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy

from .models import Workflow
from .forms import WorkflowForm


# Create your views here.
class WorkflowListView(ListView):
    model = Workflow
    template_name = "workflows/workflow_list.html"
    context_object_name = "workflows"


class WorkflowCreateView(CreateView):
    model = Workflow
    form_class = WorkflowForm
    template_name = "workflows/workflow_new.html"
    success_url = reverse_lazy("workflows:workflow_list")


class WorkflowDetailView(DetailView):
    model = Workflow
    template_name = "workflows/workflow_detail.html"
    context_object_name = "workflow"


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
