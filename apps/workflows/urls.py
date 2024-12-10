from django.urls import path
from .views import WorkflowListView, WorkflowCreateView, WorkflowDetailView, WorkflowDeleteView, WorkflowUpdateView


app_name = "workflows"
urlpatterns = [
    path("", WorkflowListView.as_view(), name="workflow_list"),
    path("new/", WorkflowCreateView.as_view(), name="workflow_new"),
    path("<int:pk>/", WorkflowDetailView.as_view(), name="workflow_detail"),
    path("<int:pk>/delete/", WorkflowDeleteView.as_view(), name="workflow_delete"),
    path("<int:pk>/edit/", WorkflowUpdateView.as_view(), name="workflow_edit"),
]
