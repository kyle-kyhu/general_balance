from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Company


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("date_joined", "company")
    list_filter = UserAdmin.list_filter + ("date_joined", "company")
    ordering = ("-date_joined",)

    fieldsets = UserAdmin.fieldsets + (("Custom Fields", {"fields": ("avatar", "company")}),)
