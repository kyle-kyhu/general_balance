from django.urls import path
from .views import WorkflowListView, WorkflowCreateView, WorkflowDetailView


app_name = "workflows"
urlpatterns = [
    path("", WorkflowListView.as_view(), name="index"),
    path("create/", WorkflowCreateView.as_view(), name="workflow_create"),
    path("<int:pk>/", WorkflowDetailView.as_view(), name="workflow_detail"),
]
