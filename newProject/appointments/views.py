
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import include, path


def appointment(request):

    return render(request, "appointments/appointment.html",)