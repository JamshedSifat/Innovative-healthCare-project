import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_group', models.CharField(
                    choices=[
                        ('A+', 'A+'), ('B+', 'B+'), ('AB+', 'AB+'), ('O+', 'O+'),
                        ('A-', 'A-'), ('B-', 'B-'), ('AB-', 'AB-'), ('O-', 'O-')
                    ],
                    max_length=20
                )),
                ('quantity', models.PositiveIntegerField()),
                ('expiry_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='doctors/', null=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('specialty', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=True)),
                ('cost', models.IntegerField()),
                ('available_spots', models.PositiveIntegerField()),
                ('next_available_appointment_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorTimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_available', models.BooleanField(default=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointments.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospital_name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('capacity', models.IntegerField()),
                ('blood_samples', models.ManyToManyField(related_name='hospitals', to='appointments.blood')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=1000)),
                ('appointment_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('serial_number', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointments.doctor')),
                ('doctor_time_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointments.doctortimeslot')),
            ],
        ),
    ]
