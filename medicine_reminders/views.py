from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import date, time
from .models import Medicine, ReminderTime, DoseTaken


@login_required
def reminders_home(request):
    """Show medicine reminders for today"""
    today = date.today()

    # Get user's active medicines
    medicines = Medicine.objects.filter(user=request.user, is_active=True)

    # Get today's schedule
    schedule = []
    for medicine in medicines:
        for reminder_time in medicine.reminder_times.all():
            # Check if already taken today
            taken = DoseTaken.objects.filter(
                medicine=medicine,
                reminder_time=reminder_time,
                date_taken=today
            ).exists()

            schedule.append({
                'medicine': medicine,
                'reminder_time': reminder_time,
                'taken': taken
            })

    return render(request, 'reminders/home.html', {
        'today_schedule': schedule,
        'active_reminders': medicines,
        'today': today
    })


@login_required
def add_reminder(request):
    """Add new medicine"""
    if request.method == 'POST':
        # Get form data
        name = request.POST['name']
        amount = request.POST['dosage_amount']
        unit = request.POST['dosage_unit']
        frequency = request.POST['frequency']
        start = request.POST['start_date']
        end = request.POST['end_date']
        notes = request.POST.get('instructions', '')

        # Create medicine
        medicine = Medicine.objects.create(
            user=request.user,
            name=name,
            dosage_amount=amount,
            dosage_unit=unit,
            frequency=frequency,
            start_date=start,
            end_date=end,
            instructions=notes
        )

        # Add reminder times
        if frequency == 'once':
            ReminderTime.objects.create(medicine=medicine, time='08:00')
        elif frequency == 'twice':
            ReminderTime.objects.create(medicine=medicine, time='08:00')
            ReminderTime.objects.create(medicine=medicine, time='20:00')
        elif frequency == 'thrice':
            ReminderTime.objects.create(medicine=medicine, time='08:00')
            ReminderTime.objects.create(medicine=medicine, time='14:00')
            ReminderTime.objects.create(medicine=medicine, time='20:00')

        messages.success(request, f"{name} added successfully!")
        return redirect('reminders:home')

    return render(request, 'reminders/add_reminder.html')


@login_required
def edit_reminder(request, medicine_id):
    """Edit medicine"""
    medicine = get_object_or_404(Medicine, id=medicine_id, user=request.user)

    if request.method == 'POST':
        medicine.name = request.POST['name']
        medicine.dosage_amount = request.POST['dosage_amount']
        medicine.dosage_unit = request.POST['dosage_unit']
        medicine.start_date = request.POST['start_date']
        medicine.end_date = request.POST['end_date']
        medicine.instructions = request.POST.get('instructions', '')
        medicine.save()

        messages.success(request, f"{medicine.name} updated!")
        return redirect('reminders:home')

    return render(request, 'reminders/edit_reminder.html', {'medicine': medicine})


@login_required
def delete_reminder(request, medicine_id):
    """Delete medicine"""
    medicine = get_object_or_404(Medicine, id=medicine_id, user=request.user)

    if request.method == 'POST':
        name = medicine.name
        medicine.delete()
        messages.success(request, f"{name} deleted!")
        return redirect('reminders:home')

    return render(request, 'reminders/delete_confirm.html', {'medicine': medicine})


@login_required
def mark_taken(request, medicine_id, reminder_time_id):
    """Mark medicine as taken"""
    if request.method == 'POST':
        medicine = get_object_or_404(Medicine, id=medicine_id)
        reminder_time = get_object_or_404(ReminderTime, id=reminder_time_id)

        # Save that medicine was taken
        DoseTaken.objects.create(
            medicine=medicine,
            reminder_time=reminder_time,
            date_taken=date.today(),
            time_taken=timezone.now().time()
        )

        messages.success(request, f"✅ {medicine.name} marked as taken!")

    return redirect('reminders:home')


@login_required
def reminder_history(request):
    """Show history of taken medicines"""
    history = DoseTaken.objects.filter(
        medicine__user=request.user
    ).order_by('-date_taken')[:50]

    return render(request, 'reminders/history.html', {'taken_doses': history})