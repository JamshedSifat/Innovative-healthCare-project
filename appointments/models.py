from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
<<<<<<< HEAD
    image = models.ImageField()
=======
    image = models.ImageField(upload_to='doctors/', null=True, blank=True)
>>>>>>> 95193974668127615266de434effc1643d28f090
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    cost = models.IntegerField()
    available_spots = models.PositiveIntegerField()
    next_available_appointment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class DoctorTimeSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
<<<<<<< HEAD

    def __str__(self):
        return f"{self.doctor.name} ({self.start_time} - {self.end_time})"
=======
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor.name} - {self.start_time} to {self.end_time}"
>>>>>>> 95193974668127615266de434effc1643d28f090

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
<<<<<<< HEAD
    doctor_time_slot = models.ForeignKey(DoctorTimeSlot, on_delete=models.CASCADE)
=======
>>>>>>> 95193974668127615266de434effc1643d28f090
    description = models.CharField(max_length=1000)
    appointment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    serial_number = models.PositiveIntegerField(default=0)

    def __str__(self):
<<<<<<< HEAD
        return self.user.username

class Hospital(models.Model):
    hospital_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()
    blood_samples = models.ManyToManyField('Blood', related_name='hospitals')

    def __str__(self):
        return self.hospital_name

class Blood(models.Model):
    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'), ('B+', 'B+'), ('AB+', 'AB+'), ('O+', 'O+'),
        ('A-', 'A-'), ('B-', 'B-'), ('AB-', 'AB-'), ('O-', 'O-'),
    )
    blood_group = models.CharField(max_length=20, choices=BLOOD_GROUP_CHOICES)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()

    def __str__(self):
        return f"{self.blood_group}"
=======
        return f"{self.user.username} - {self.doctor.name}"
>>>>>>> 95193974668127615266de434effc1643d28f090
