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
        required=False, widget=forms.FileInput(attrs={"class": "form-control", "accept": ".xlsx,.xls"})
    )

    data_file = forms.FileField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control", "accept": ".csv"})
    )

    script_file = forms.FileField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control", "accept": ".py"})
    )

    class Meta:
        model = Workflow
        fields = ["name", "description", "data_source", "template_file", "data_file", "script_file"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "input input-bordered w-full", "placeholder": "Enter workflow name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 4,
                    "placeholder": "Enter workflow description",
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long")
        return name

    def clean_script_file(self):
        script_file = self.cleaned_data.get("script_file")
        if script_file and not script_file.name.endswith(".py"):
            raise forms.ValidationError("Only Python (.py) files are allowed")
        return script_file

    def clean_template_file(self):
        template_file = self.cleaned_data.get("template_file")
        if template_file and not template_file.name.endswith((".xlsx", ".xls")):
            raise forms.ValidationError("Only Excel files (.xlsx, .xls) are allowed")
        return template_file

    def clean_data_file(self):
        data_file = self.cleaned_data.get("data_file")
        data_source = self.cleaned_data.get("data_source")
        if data_source == "csv" and data_file and not data_file.name.endswith(".csv"):
            raise forms.ValidationError("Only CSV files are allowed")
        return data_file
