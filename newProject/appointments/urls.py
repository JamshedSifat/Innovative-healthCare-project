from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointment, name='appointment'),
    path('search/', views.doctor_search, name='doctor_search'),
    path('create/<int:doctor_id>/', views.create_appointment, name='create_appointment'),
]