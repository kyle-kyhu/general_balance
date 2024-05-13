from django.urls import path

from .views import AmwellListView, BankRecView, BankRecScriptView, BankRecDownloadView

app_name = "amwell"

urlpatterns = [
    path("", AmwellListView.as_view(), name="list"),
    path("bank_rec/", BankRecView.as_view(), name="bank_rec"),
    path("bank_rec/script/", BankRecScriptView.as_view(), name="bank_rec_script"),
    path("bank_rec/download/", BankRecDownloadView.as_view(), name="bank_rec_download"),
]