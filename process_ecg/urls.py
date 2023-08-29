from django.urls import path
from . import views
urlpatterns = [
    path("", views.process_ecg_data, name="ecg_data")
]