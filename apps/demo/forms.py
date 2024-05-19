from django import forms
from .models import CsvTask

class CsvFileForm(forms.ModelForm):
    class Meta:
        model = CsvTask
        fields = ['csv_file']

class ExcelFileForm(forms.ModelForm):
    class Meta:
        model = CsvTask
        fields = ['excel_file']
        