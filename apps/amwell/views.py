from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, View, FormView
from django.shortcuts import redirect
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
        return context

    def get_queryset(self):
        csv_file = BankRec.objects.all()
        excel_file = BankRec.objects.all()
        return {'csv_file': csv_file, 'excel_file': excel_file}


class BankRecView(FormView):
    template_name = "amwell/bank_rec.html"
    form_class = CsvFileForm
    excel_form = ExcelFileForm
    success_url = '/amwell/bank_rec/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file_instance = BankRec.objects.last()  # Get the most recent file
        context.update({
            'excel_form': self.excel_form(self.request.POST or None, self.request.FILES or None),
            'file': file_instance,
            'show_run_script': self.request.session.pop('show_run_script', False),
            'script_executed': self.request.session.get('script_executed', False)
        })
        return context
    
    def get_form(self, form_class=None):
        form_class = self.form_class
        form = super().get_form(form_class)
        return form

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        excel_form = self.excel_form(self.request.POST, self.request.FILES)
        if form.is_valid() and excel_form.is_valid():
            return self.form_valid(form, excel_form)
        else:
            return self.form_invalid(form, excel_form)

    def form_valid(self, excel_form, form):
        excel_form.save()
        form.save()
        messages.success(self.request, 'Files uploaded successfully')
        self.request.session['show_run_script'] = True
        return super().form_valid(excel_form) 
    


class BankRecScriptView(View):
    def post(self, request, *args, **kwargs):
        # Check if there are files uploaded
        file_instance = BankRec.objects.filter(csv_file__isnull=False, excel_file__isnull=False).last()
        
        if not file_instance:
            messages.error(request, "No files uploaded.")
            return redirect('amwell:bank_rec')

        # Define paths
        base_dir = os.path.join(settings.BASE_DIR, 'media', 'static', 'bank_rec')
        script_path = os.path.join(base_dir, 'sandbox1.py')  # sandbox1.py is the script file
        csv_file_path = os.path.join(base_dir, file_instance.csv_file.name)  # csv_file is a FileField
        excel_file_path = os.path.join(base_dir, file_instance.excel_file.name) # excel_file is a FileField
        
        print("CSV File Path:", csv_file_path)
        print("Excel File Path:", excel_file_path)


        # Check if script file exists
        if not os.path.isfile(script_path):
            messages.error(request, f'Script file not found: {script_path}')
            return redirect('amwell:bank_rec')
        
        # Run the script
        try:
            result = subprocess.run(['python', script_path, csv_file_path, excel_file_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("STDOUT:", result.stdout.decode())
            print("STDERR:", result.stderr.decode())

            if result.returncode == 0:
                messages.success(request, 'Script executed successfully')
                # Assuming script modifies the existing Excel file or creates a new one in the same path
                file_instance.updated_excel_file = excel_file_path # create or update the updated_excel_file filefield in model
                file_instance.save()
        except subprocess.CalledProcessError as e:
            messages.error(request, f'Error while executing script: {e}')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {e}')

        return redirect('amwell:bank_rec')

class BankRecDownloadView(View):
    def get (self, request, *args, **kwargs):
        updated_instance = BankRec.objects.last()
        if updated_instance:
            file_path = updated_instance.updated_excel_file
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
    

