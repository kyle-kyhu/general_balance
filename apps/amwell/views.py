from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, View, FormView
import os
import subprocess
import glob

from .models import BankRec
from .forms import CsvFileForm, ExcelFileForm


class AmwellListView(ListView):
    template_name = "amwell/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['csv_file'] = BankRec.objects.all()
        context['excel_file'] = BankRec.objects.all()
        # context["csv_file_form"] = CsvFileForm()
        # context["excel_file_form"] = ExcelFileForm()
        return context

    def get_queryset(self):
        csv_file = BankRec.objects.all()
        excel_file = BankRec.objects.all()
        return {'csv_file': csv_file, 'excel_file': excel_file}


class BankRecView(FormView):
    template_name = "amwell/bankrec.html"
    csv_form = CsvFileForm
    excel_form = ExcelFileForm
    

    """ this function is calling the data to be displayed on the page. """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file_instance = BankRec.objects.last()  # Get the most recent file
        context.update({
            'excel_form': self.excel_form(self.request.POST, self.request.FILES),
            'file': file_instance,
            'show_run_script': self.request.session.pop('show_run_script', False),
            'script_executed': self.request.session.get('script_executed', False)
        })
        return context
    
    """ this function is posting the forms to the database. """
    def post(self, request, *args, **kwargs):
        csv_form = self.get_form()
        excel_form = self.excel_form_class(self.request.POST, self.request.FILES)
        if csv_form.is_valid() and excel_form.is_valid():
            return self.form_valid(csv_form, excel_form)
        else:
            return self.form_invalid(csv_form, excel_form)

    """is fuction is saving the forms to the database."""
    def form_valid(self, excel_form, csv_form):
        excel_form.save()
        csv_form.save()
        messages.success(self.request, 'Files uploaded successfully')
        self.request.session['show_run_script'] = True
        return super().form_valid(excel_form) # potential issue.  formview is expecting instance. 

'''This view is for running the python script to update the excel file.'''
class BankRecScriptView(View):
    def post(self, request, *args, **kwargs):
        file_instance = BankRec.objects.last()
        if file_instance:
            script_path = os.path.join(settings.MEDIA_ROOT, 'files/sandbox1.py')
            # Check if the script file exists
            if not os.path.isfile(script_path):
                messages.error(request, f'Script file not found: {script_path}')
                return render(request, 'amwell/bank_rec.html')

            try:
                env = os.environ.copy()
                env['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'
                result = subprocess.run(['python', script_path, file_instance.file.path], check=True, env=env)
                if result.returncode == 0:
                    messages.success(request, 'Yay, Script executed successfully')
                    excel_files = glob.glob(os.path.join(settings.MEDIA_ROOT, 'files/*.xlsx'))
                    # Check if there are any Excel files
                    if excel_files:
                        # Select the most recent Excel file
                        most_recent_excel_path = max(excel_files, key=os.path.getctime)
                        file_instance.updated_excel_file = most_recent_excel_path
                        file_instance.save()
                        request.session['script_executed'] = True
                    else:
                        messages.error(request, 'No excel file found')
            except subprocess.CalledProcessError as e:
                messages.error(request, f'Error while executing script: {e}')
            except Exception as e:
                messages.error(request, f'An unexpected error occurred: {e}')
        return render(request, 'amwell/bank_rec.html')


# this class get the updated excel file and download it
class BankRecDownloadView(View):
    def get (self, request, *args, **kwargs):
        file_instance = BankRec.objects.last()
        if file_instance:
            file_path = file_instance.updated_excel_file
            if file_path and os.path.isfile(file_path):
                try:
                    with open(file_path, 'rb') as file:
                        response = HttpResponse(file.read(), content_type='application/vnd.ms-excel')
                        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                        return response
                except IOError:
                    messages.error(request, 'Error opening file')
            else:
                messages.error(request, 'No updated excel file found')
        return render(request, 'amwell/bank_rec.html')