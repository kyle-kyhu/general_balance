from django.db import models
import logging

logger = logging.getLogger(__name__)


def workflow_directory_path(instance, filename):
    # Add logging to debug the path creation
    path = f"workflows/{instance.id}/{filename}"
    print(f"Creating path for file: {path}")  # This will show in your console
    return path


class Workflow(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    data_source = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    data_file = models.FileField(upload_to=workflow_directory_path, null=True, blank=True)

    script_file = models.FileField(upload_to=workflow_directory_path, null=True, blank=True)

    latest_output_file = models.CharField(max_length=255, blank=True, null=True)

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

    def save(self, *args, **kwargs):
        # Add logging when saving
        print(f"Saving workflow {self.id} with files:")
        print(f"Template: {self.template_file.name if self.template_file else 'None'}")
        print(f"Data: {self.data_file.name if self.data_file else 'None'}")
        print(f"Script: {self.script_file.name if self.script_file else 'None'}")
        super().save(*args, **kwargs)
