from django.urls import path

from .views import (
    ListView, 
    CsvDetailedView,
    CsvScriptView, 
    CsvDownloadView,
    NewsView,
    StreamlitView,
)

app_name = "demo"

urlpatterns = [
    path("", ListView.as_view(), name="demo_list"),
    path("csv/", CsvDetailedView.as_view(), name="demo_csv"),
    path("csv/script/", CsvScriptView.as_view(), name="demo_script"),
    path("csv/download/", CsvDownloadView.as_view(), name="demo_download"),
    path("news/", NewsView.as_view(), name="demo_news"),
    # do you want other weather api urls?
    path('streamlit/', StreamlitView.as_view(), name='demo_streamlit'),
]