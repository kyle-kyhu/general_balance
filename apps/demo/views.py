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

from .models import CsvTask
from .forms import CsvFileForm, ExcelFileForm


class ListView(ListView):
    template_name = "demo/demo_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['csv_file'] = CsvTask.objects.all()
        context['excel_file'] = CsvTask.objects.all()
        return context

    def get_queryset(self):
        return CsvTask.objects.all()
    
class CsvDetailedView(FormView):
    template_name = "demo/demo_csv.html"
    form_class = CsvFileForm
    excel_form_class = ExcelFileForm
    success_url = '/demo/csv/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file_instance = CsvTask.objects.last()
        context.update({
            'excel_form': self.excel_form_class(self.request.POST or None, self.request.FILES or None),
            'file': file_instance,
            'show_run_script': self.request.session.pop('show_run_script', False),
            'script_executed': self.request.session.pop('script_executed', False),
            'download_file_name': os.path.basename(file_instance.updated_excel_file.name) 
            if file_instance and file_instance.updated_excel_file else None,
        })
        return context
    
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.form_class
        return super().get_form(form_class)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        excel_form = self.excel_form_class(self.request.POST, self.request.FILES)
        if form.is_valid() and excel_form.is_valid():
            return self.form_valid(form, excel_form)
        else:
            return self.form_invalid(form, excel_form)
    
    def form_valid(self, form, excel_form):
        form.save()
        excel_form.save()
        messages.success(self.request, "Files uploaded successfully")
        self.request.session['show_run_script'] = True
        return super().form_valid(form)
    
    def form_invalid(self, form, excel_form):
        return self.render_to_response(self.get_context_data(form=form, excel_form=excel_form))
    

class CsvScriptView(View):
    def post(self, request, *args, **kwargs):
        file_instance = CsvTask.objects.filter(
            csv_file__isnull=False, 
            excel_file__isnull=False).last()
    
        if not file_instance:
            messages.error(request, "Please upload both CSV and Excel files first")
            return redirect('demo:demo_csv')
        
        base_dir = os.path.join(settings.MEDIA_ROOT, 'static', 'demo', 'csv_task')
        script_path = os.path.join(base_dir, 'sandbox1.py')
        csv_file = os.path.join(base_dir, os.path.basename(file_instance.csv_file.name))
        excel_file = os.path.join(base_dir, os.path.basename(file_instance.excel_file.name))

        if not os.path.exists(script_path):
            messages.error(request, "Script not found")
            return redirect('demo:demo_csv')
        
        try:
            env = os.environ.copy()
            env['DJANGO_SETTINGS_MODULE'] = 'general_balance.settings'

            result = subprocess.run(
                ['python', script_path, csv_file, excel_file], 
                check=True, 
                env=env, 
                capture_output=True, 
                text=True,
                )
            if result.returncode == 0:
                messages.success(request, "Script executed successfully")
                excel_files = glob.glob(os.path.join(base_dir, '*.xlsx'))
                if excel_files:
                    most_recent_excel_path = max(excel_files, key=os.path.getctime)
                    file_instance.updated_excel_file = os.path.relpath(most_recent_excel_path, settings.MEDIA_ROOT)
                    file_instance.python_script_success = True
                    file_instance.save()
                    request.session['downloadable_file'] = most_recent_excel_path
                else:
                    if 'downloadable_file' in request.session:
                        del request.session['downloadable_file']
            else:
                messages.error(request, 'Error while executing script')
        except subprocess.CalledProcessError as e:
            messages.error(request, f'Error while executing script: {e}')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {e}')

        return redirect('demo:demo_csv')
    
class CsvDownloadView(View):
    def get(self, request, *args, **kwargs):
        file_path = request.session.get('downloadable_file')
        if file_path and os.path.isfile(file_path):
            try:
                with open(file_path, 'rb') as file:
                    response = HttpResponse(file.read(), content_type='application/vnd.ms-excel')
                    file_name = os.path.basename(file_path)
                    response['Content-Disposition'] = f'attachment; filename={file_name}'
                    return response
            except IOError:
                messages.error(request, 'Error opening file')
        else:
            messages.error(request, 'No updated excel file found')
        return redirect('demo:demo_csv')