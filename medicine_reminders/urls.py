from django.urls import path
from . import views

app_name = 'reminders'  # Keep the namespace as 'reminders' for URL reversing

urlpatterns = [
    path('', views.reminders_home, name='home'),
    path('add/', views.add_reminder, name='add_reminder'),
    path('edit/<int:medicine_id>/', views.edit_reminder, name='edit_reminder'),
    path('delete/<int:medicine_id>/', views.delete_reminder, name='delete_reminder'),
    path('mark-taken/<int:medicine_id>/<int:reminder_time_id>/', views.mark_taken, name='mark_taken'),
    path('history/', views.reminder_history, name='history'),
]