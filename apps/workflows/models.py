from django.db import models
from django.utils.text import slugify


def workflow_directory_path(instance, filename):
    # Files will be uploaded to MEDIA_ROOT/workflows/<workflow_slug>/<filename>
    return f"workflows/{instance.slug}/{filename}"


class Workflow(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()

    # Required files
    template_file = models.FileField(
        upload_to=workflow_directory_path, help_text="Excel template file that will be used"
    )
    script_file = models.FileField(upload_to=workflow_directory_path, help_text="Python script that processes the data")

    # Data source - only one should be used
    DATA_SOURCE_CHOICES = [
        ("CSV", "CSV File"),
        ("EXCEL", "Excel File"),
        ("NETSUITE", "NetSuite API"),
    ]
    data_source = models.CharField(max_length=10, choices=DATA_SOURCE_CHOICES, default="EXCEL")

    # Optional data files based on source type
    data_file = models.FileField(
        upload_to=workflow_directory_path, null=True, blank=True, help_text="Data file (CSV or Excel) if applicable"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_workflow_directory(self):
        return f"workflows/{self.slug}"
