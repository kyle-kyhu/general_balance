from django.contrib import admin
from .models import BankRec


class BankRecAdmin(admin.ModelAdmin):
    list_display = (
        'csv_file', 
        'excel_file', 
        'updated_excel_file', 
        'csv_file_uploaded_at', 
        'excel_file_uploaded_at', 
        'python_script_success',
        )
    list_filter = (
        'excel_file_uploaded_at',
          'python_script_success',
          )
    


admin.site.register(BankRec, BankRecAdmin)