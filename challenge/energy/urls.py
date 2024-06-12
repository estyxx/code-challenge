from django.urls import path

from . import views

urlpatterns = [
    path("upload-csv/", views.upload_csv, name="upload_csv"),
    path("upload-success/", views.upload_success, name="upload_success"),
]
