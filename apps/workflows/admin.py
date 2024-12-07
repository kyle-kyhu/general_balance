from django.contrib import admin
from .models import Workflow


class workflowAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")


admin.site.register(Workflow, workflowAdmin)
