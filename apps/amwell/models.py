from django.db import models

class BankRec(models.Model):
    csv_file = models.FileField(upload_to='static/bank_rec/')
    excel_file = models.FileField(upload_to='static/bank_rec/')
    updated_excel_file = models.FileField(upload_to='static/bank_rec/', blank=True, null=True)
    csv_file_uploaded_at = models.DateTimeField(auto_now_add=True)
    excel_file_uploaded_at = models.DateTimeField(auto_now_add=True)
    python_script_success = models.BooleanField(default=False)

    def __str__(self):
        return f"CSV: {self.csv_file.name}, Excel: {self.excel_file.name}"