from django.views.generic import ListView
from .models import excel_data_workflow


# Create your views here.
class IndexListView(ListView):
    model = excel_data_workflow
    template_name = "workflows/workflow_list.html"
    context_object_name = "workflows"
