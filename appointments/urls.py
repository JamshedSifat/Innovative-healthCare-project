from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointment, name='appointment'),
    path('search/', views.doctor_search, name='doctor_search'),
    path('create/<int:doctor_id>/', views.create_appointment, name='create_appointment'),
<<<<<<< HEAD
    path('cancel/<int:appointment_id>/<int:doctor_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('emergency/', views.emergency, name='emergency'),
    path('emergency/search/', views.blood_search, name='blood_search'),
]
=======
]
>>>>>>> 95193974668127615266de434effc1643d28f090
