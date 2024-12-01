from django.contrib import admin
from .models import excel_data_workflow


class excel_data_workflowAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")


admin.site.register(excel_data_workflow, excel_data_workflowAdmin)
