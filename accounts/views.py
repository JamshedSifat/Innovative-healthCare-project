from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm, UserForm
import random
from django.core.mail import send_mail
from django.conf import settings


def register(request):
    if request.method == 'POST':
        username = request.POST.get('u_name')
        first_name = request.POST.get('u_fname')
        last_name = request.POST.get('u_lname')
        email = request.POST.get('u_email')
        password = request.POST.get('u_password')
        age = request.POST.get('u_age')
        address = request.POST.get('u_address')
        mobile = request.POST.get('u_mobile')
        gender = request.POST.get('u_gender')

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'accounts/register.html')

        # Generate OTP
        otp = str(random.randint(100000, 999999))

        # Store registration data in session
        request.session['registration_data'] = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'age': age,
            'address': address,
            'mobile': mobile,
            'gender': gender,
            'otp': otp
        }

        # Send OTP email (you'll need to configure email settings)
        try:
            send_mail(
                'Registration OTP',
                f'Your OTP is: {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return redirect('accounts:verify_otp')
        except:
            messages.error(request, 'Error sending OTP. Please try again.')
            return render(request, 'accounts/register.html')

    return render(request, 'accounts/register.html')


def verify_otp(request):
    if 'registration_data' not in request.session:
        messages.error(request, 'Registration session expired')
        return redirect('accounts:register')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session['registration_data'].get('otp')

        if entered_otp == stored_otp:
            # Create user and profile
            data = request.session['registration_data']
            user = User.objects.create_user(
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password']
            )

            UserProfile.objects.create(
                user=user,
                age=data['age'],
                address=data['address'],
                mobile=data['mobile'],
                gender=data['gender']
            )

            del request.session['registration_data']
            messages.success(request, 'Registration successful! Please login.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Invalid OTP')

    email = request.session['registration_data'].get('email', '')
    return render(request, 'accounts/verify_otp.html', {'email': email})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('u_name')
        password = request.POST.get('u_password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        if 'delete_account' in request.POST:
            request.user.delete()
            messages.success(request, 'Account deleted successfully')
            return redirect('home')
        else:
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = UserProfileForm(request.POST, instance=user_profile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Profile updated successfully')
                return redirect('accounts:user_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)


    appointments = []
    bills = []

    context = {
        'user_profile': user_profile,
        'user_form': user_form,
        'profile_form': profile_form,
        'appointments': appointments,
        'bills': bills,
    }
    return render(request, 'accounts/user_profile.html', context)