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
        return BankRec.objects.all()  

class BankRecView(FormView):
    template_name = "amwell/bank_rec.html"
    form_class = CsvFileForm
    excel_form_class = ExcelFileForm
    success_url = '/amwell/bank_rec/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file_instance = BankRec.objects.last()  # Get the most recent file
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
        messages.success(self.request, 'Files uploaded successfully')
        self.request.session['show_run_script'] = True
        return super().form_valid(form)

    def form_invalid(self, form, excel_form):
        return self.render_to_response(self.get_context_data(form=form, excel_form=excel_form))


class BankRecScriptView(View):
    def post(self, request, *args, **kwargs):
        file_instance = BankRec.objects.filter(
            csv_file__isnull=False, 
            excel_file__isnull=False).last()

        if not file_instance:
            messages.error(request, "No files uploaded.")
            return redirect('amwell:bank_rec')

        base_dir = os.path.join(settings.MEDIA_ROOT, 'static', 'bank_rec')  # Ensure the correct base directory
        script_path = os.path.join(base_dir, 'sandbox1.py')
        csv_file_path = os.path.join(base_dir, os.path.basename(file_instance.csv_file.name))  # Ensure full path to CSV file
        excel_file_path = os.path.join(base_dir, os.path.basename(file_instance.excel_file.name))  # Ensure full path to Excel file

        print("CSV File Path:", csv_file_path)
        print("Excel File Path:", excel_file_path)
        print("Script Path:", script_path)

        if not os.path.isfile(script_path):
            messages.error(request, f'Script file not found: {script_path}')
            return redirect('amwell:bank_rec')

        try:
            env = os.environ.copy()
            env['DJANGO_SETTINGS_MODULE'] = 'general_balance.settings'

            # Print the Python script being run
            print("Running Python script:", script_path)

            result = subprocess.run(['python', script_path, csv_file_path, excel_file_path], 
                                    check=True, 
                                    env=env, 
                                    capture_output=True, 
                                    text=True,
                                    )
            
            print("Subprocess STDOUT:", result.stdout)
            print("Subprocess STDERR:", result.stderr)

            if result.returncode == 0:
                messages.success(request, 'Script executed successfully')
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

        return redirect('amwell:bank_rec')





class BankRecDownloadView(View):
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
        return redirect('amwell:bank_rec')

'''OLD'''
# class BankRecScriptView(View):
#     def post(self, request, *args, **kwargs):
#         # Check if there are files uploaded
#         file_instance = BankRec.objects.filter(csv_file__isnull=False, excel_file__isnull=False).last()
        
#         if not file_instance:
#             messages.error(request, "No files uploaded.")
#             return redirect('amwell:bank_rec')

#         # Define paths
#         base_dir = os.path.join(settings.BASE_DIR, 'media', 'static', 'bank_rec')
#         script_path = os.path.join(base_dir, 'sandbox1.py')  # sandbox1.py is the script file
#         csv_file_path = os.path.join(base_dir, file_instance.csv_file.name)  # csv_file is a FileField
#         excel_file_path = os.path.join(base_dir, file_instance.excel_file.name) # excel_file is a FileField
        
#         print("CSV File Path:", csv_file_path)
#         print("Excel File Path:", excel_file_path)


#         # Check if script file exists
#         if not os.path.isfile(script_path):
#             messages.error(request, f'Script file not found: {script_path}')
#             return redirect('amwell:bank_rec')
        
#         # Run the script
#         try:
#             result = subprocess.run(['python', script_path, csv_file_path, excel_file_path],
#                                      check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             print("STDOUT:", result.stdout.decode())
#             print("STDERR:", result.stderr.decode())

#             if result.returncode == 0:
#                 messages.success(request, 'Script executed successfully')
#                 # Assuming script modifies the existing Excel file or creates a new one in the same path
#                 relative_path = os.path.join('static', 'bank_rec', os.path.basename(excel_file_path))
#                 file_instance.updated_excel_file = relative_path
#                 # create or update the updated_excel_file filefield in model
#                 #file_instance.updated_excel_file = excel_file_path 
#                 file_instance.python_script_success = True # update model
#                 file_instance.save()
#                 self.request.session['script_executed'] = True
#                 request.session['download_file'] = str(file_instance.updated_excel_file)
#             else:
#                 messages.error(request, 'Error while executing script')
#         except subprocess.CalledProcessError as e:
#             messages.error(request, f'Error while executing script: {e}')
#         except Exception as e:
#             messages.error(request, f'An unexpected error occurred: {e}')

#         return redirect('amwell:bank_rec')

# class BankRecDownloadView(View):
#     def get (self, request, *args, **kwargs):
#         file_path = request.session.get('download_file')
#         if file_path and os.path.isfile(file_path):
#             try:
#                 with open(file_path, 'rb') as file:
#                     response = HttpResponse(file.read(), content_type='application/vnd.ms-excel')
#                     file_name = os.path.basename(file_path)  # Get the file name
#                     response['Content-Disposition'] = f'attachment; filename={file_name}'
#                     return response
#             except IOError:
#                 messages.error(request, 'Error opening file')
#         else:
#             messages.error(request, 'No updated excel file found')
#         return render(request, 'amwell/bank_rec.html')

