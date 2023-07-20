from django.urls import path
from . import views
urlpatterns = [
    path("", views.get_hb_data, name="hb_data")
]