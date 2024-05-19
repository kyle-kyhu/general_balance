from django.urls import path

from .views import (
    ListView, 
    CsvDetailedView,
    CsvScriptView, 
    CsvDownloadView,
)

app_name = "demo"

urlpatterns = [
    path("demo", ListView.as_view(), name="demo_list"),
    path("csv/", CsvDetailedView.as_view(), name="demo_csv"),
    path("csv/script/", CsvScriptView.as_view(), name="demo_script"),
    path("csv/download/", CsvDownloadView.as_view(), name="demo_download"),
]