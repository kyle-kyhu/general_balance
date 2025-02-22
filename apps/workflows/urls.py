from django.urls import path
from . import views

app_name = "workflows"

urlpatterns = [
    path("", views.WorkflowListView.as_view(), name="workflow_list"),
    path("new/", views.WorkflowCreateView.as_view(), name="workflow_new"),
    path("<int:pk>/", views.WorkflowDetailView.as_view(), name="workflow_detail"),
    path("<int:pk>/edit/", views.WorkflowUpdateView.as_view(), name="workflow_edit"),
    path("<int:pk>/delete/", views.WorkflowDeleteView.as_view(), name="workflow_delete"),
    path("<int:pk>/validate/", views.validate_files, name="validate_files"),
    path("<int:workflow_id>/download-script/", views.download_script, name="download_script"),
]
