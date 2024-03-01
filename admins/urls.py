from django.urls import re_path
from . import views

app_name = "admins"

urlpatterns = [
    re_path(r"^$", views.index, name = "admin_index"),
]
