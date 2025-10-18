from django.contrib import admin
<<<<<<< HEAD
from .models import *

admin.site.register(Doctor)
admin.site.register(DoctorTimeSlot)
admin.site.register(Appointment)
admin.site.register(Hospital)
admin.site.register(Blood)
=======
from .models import Doctor, Appointment, DoctorTimeSlot

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty', 'status', 'cost', 'available_spots']
    list_filter = ['specialty', 'status']
    search_fields = ['name', 'specialty']

@admin.register(DoctorTimeSlot)
class DoctorTimeSlotAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'start_time', 'end_time', 'is_available']
    list_filter = ['doctor', 'is_available']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'doctor', 'appointment_date', 'created_at']
    list_filter = ['appointment_date', 'doctor']
    search_fields = ['user__username', 'doctor__name']
>>>>>>> 95193974668127615266de434effc1643d28f090
