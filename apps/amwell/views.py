from django.shortcuts import render

from django.views import View
from django.views.generic import ListView, View, FormView

from .models import BankRec
from .forms import CsvFileForm, ExcelFileForm


class AmwellListView(ListView):
    pass
    # template_name = "amwell/list.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["csv_file_form"] = CsvFileForm()
    #     context["excel_file_form"] = ExcelFileForm()
    #     return context

    # def get_queryset(self):
    #     return BankRec.objects.all()


class BankRecView(FormView):
    pass

class BankRecScriptView(View):
    pass

class BankRecDownloadView(View):
    pass