from django import forms
from .models import Workflow


class WorkflowForm(forms.ModelForm):
    class Meta:
        model = Workflow
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter workflow name"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Enter workflow description"}
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long")
        return name
