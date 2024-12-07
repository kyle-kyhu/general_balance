from django.views.generic import ListView, CreateView, DetailView
from .models import Workflow


# Create your views here.
class WorkflowListView(ListView):
    model = Workflow
    template_name = "workflows/workflow_list.html"
    context_object_name = "workflows"


class WorkflowCreateView(CreateView):
    model = Workflow
    template_name = "workflows/workflow_create.html"
    fields = ["name", "description"]


class WorkflowDetailView(DetailView):
    model = Workflow
    template_name = "workflows/workflow_detail.html"
    context_object_name = "workflow"
