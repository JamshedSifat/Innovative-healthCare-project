from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .models import *


def appointment(request):
    doctors = Doctor.objects.all()
    return render(request, "appointments/appointment.html", {'doctors': doctors})


def doctor_search(request):
    query_d = request.GET.get('q')

    if query_d:
        words = query_d.split()
        name_query = Q()
        specialty_query = Q()
        status_query = Q()

        for word in words:
            if word.lower() == "available":
                status_query = Q(status=True)
            elif word.lower() == "unavailable":
                status_query = Q(status=False)
            else:
                name_query |= Q(name__icontains=word)
                specialty_query |= Q(specialty__icontains=word)

        doctors = Doctor.objects.filter(name_query | specialty_query, status_query)
    else:
        messages.error(request, "Search bar was empty")
        return redirect('appointments:appointment')

    if not doctors:
        messages.error(request, "No doctors found.")
        return redirect('appointments:appointment')

    return render(request, 'appointments/appointment.html', {'doctors': doctors})


@login_required
def create_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        description = request.POST.get('description', '')
        appointment_date = request.POST.get('appointment_date')

        if not appointment_date:
            messages.error(request, "Please select an appointment date.")
            return redirect('appointments:appointment')

        # Check if doctor has available spots
        if doctor.available_spots <= 0:
            messages.error(request, "No available spots for this doctor.")
            return redirect('appointments:appointment')

        # Create appointment
        appointment = Appointment.objects.create(
            user=request.user,
            doctor=doctor,
            description=description,
            appointment_date=appointment_date,
            serial_number=Appointment.objects.filter(doctor=doctor, appointment_date=appointment_date).count() + 1
        )

        # Decrease available spots
        doctor.available_spots -= 1
        doctor.save()

        messages.success(request, f"Appointment booked successfully with Dr. {doctor.name}")
        return redirect('appointments:appointment')

    return render(request, 'appointments/create_appointment.html', {'doctor': doctor})