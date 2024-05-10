from django.db import models

class BankRec(models.Model):
    csv_file = models.FileField(upload_to='static/all_files/')
    excel_file = models.FileField(upload_to='static/all_files/')
    updated_excel_file = models.FileField(upload_to='static/all_files/', null=True, blank=True)
    csv_file_uploaded_at = models.DateTimeField(auto_now_add=True)
    excel_file_uploaded_at = models.DateTimeField(auto_now_add=True)
    python_script_success = models.BooleanField(default=False)

    def __str__(self):
        return self.csv_file.name, self.excel_file.name