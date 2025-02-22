from django import forms
from .models import Workflow

DATA_TYPE_CHOICES = [
    ("csv", "CSV"),
    ("excel", "Excel"),
    ("netsuite", "NetSuite"),
    ("salesforce", "Salesforce"),
]


class WorkflowForm(forms.ModelForm):
    data_source = forms.ChoiceField(
        choices=DATA_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "select select-bordered w-full", "placeholder": "Select data source"}),
    )

    template_file = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            }
        ),
    )

    data_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control", "accept": ".csv"}),
    )

    class Meta:
        model = Workflow
        fields = ["name", "description", "data_source", "template_file", "data_file"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long")
        return name

    def clean_template_file(self):
        file = self.cleaned_data.get("template_file")
        if file:
            if not file.name.lower().endswith(".xlsx"):
                raise forms.ValidationError("Only Excel (.xlsx) files are allowed.")
            content_type = file.content_type
            if content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                raise forms.ValidationError("Invalid Excel file format. Please use .xlsx format.")
        return file

    def clean_data_file(self):
        file = self.cleaned_data.get("data_file")
        if file:
            if not file.name.endswith(".csv"):
                raise forms.ValidationError("Only CSV files are allowed.")
        return file


class ScriptUploadForm(forms.Form):
    script_file = forms.FileField(
        widget=forms.FileInput(attrs={"class": "form-control", "accept": ".py"}),
        label="Python Script",
    )

    def clean_script_file(self):
        file = self.cleaned_data.get("script_file")
        if file:
            if not file.name.endswith(".py"):
                raise forms.ValidationError("Only Python (.py) files are allowed.")
        return file
