from django import forms
from .models import BankRec

class CsvFileForm(forms.ModelForm):
    class Meta:
        model = BankRec
        fields = ['csv_file']

class ExcelFileForm(forms.ModelForm):
    class Meta:
        model = BankRec
        fields = ['excel_file']