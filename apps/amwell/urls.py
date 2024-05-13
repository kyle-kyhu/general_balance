from django.urls import path

from .views import AmwellListView, BankRecView, BankRecScriptView, BankRecDownloadView

app_name = "amwell"

urlpatterns = [
    path("", AmwellListView.as_view(), name="list"),
    path("bankrec/", BankRecView.as_view(), name="bank_rec"),
    path("bankrec/script/", BankRecScriptView.as_view(), name="bank_rec_script"),
    path("bankrec/download/", BankRecDownloadView.as_view(), name="bank_rec_download"),
]