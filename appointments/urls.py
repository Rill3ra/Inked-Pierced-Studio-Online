# appointments/urls.py
from django.urls import path
from . import views

app_name = 'appointments'  # Namespace для URL-адресов

urlpatterns = [
    path('create/', views.appointment_create, name='appointment_create'),
    path('list/', views.appointment_list, name='appointment_list'),
]