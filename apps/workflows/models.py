from django.db import models
import logging

logger = logging.getLogger(__name__)


def workflow_directory_path(instance, filename):
    # Files will be uploaded to MEDIA_ROOT/workflows/<id>/<filename>
    path = f"workflows/{instance.id}/{filename}"
    logger.info(f"Saving file to: {path}")
    return path


class Workflow(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Data source choices
    DATA_SOURCE_CHOICES = [
        ("csv", "CSV File"),
        ("excel", "Excel File"),
        ("netsuite", "NetSuite API"),
        ("salesforce", "Salesforce API"),
    ]

    data_source = models.CharField(
        max_length=20,
        choices=DATA_SOURCE_CHOICES,
        default="csv",
        help_text="Select the type of data source for this workflow",
    )

    template_file = models.FileField(upload_to=workflow_directory_path, null=True, blank=True)

    data_file = models.FileField(
        upload_to=workflow_directory_path, null=True, blank=True, help_text="Data file (CSV or Excel) if applicable"
    )

    script_file = models.FileField(upload_to=workflow_directory_path, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_workflow_directory(self):
        return f"workflows/{self.id}"

    def save_script(self, script_file):
        """Save a new script file to the workflow"""
        self.script_file = script_file
        self.save()

    def get_script_path(self):
        """Get the path to the script file"""
        if self.script_file:
            return self.script_file.path
        return None
