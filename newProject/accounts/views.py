from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Prefetch, Sum
from django.shortcuts import redirect, render

from .forms import UserForm, UserProfileForm
from .models import UserProfile



def login(request):
    if request.method == "POST":
        username = request.POST.get("u_name")
        password = request.POST.get("u_password")

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect("accounts:login")

        authenticated_user = authenticate(request, username=username, password=password)

        if authenticated_user is not None:
            auth_login(request, authenticated_user)
            messages.success(request, f"Welcome, {username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


def register(request):
    if request.method == "POST":
        u_name = request.POST.get("u_name")
        u_fname = request.POST.get("u_fname")
        u_lname = request.POST.get("u_lname")
        u_email = request.POST.get("u_email")
        u_password = request.POST.get("u_password")
        u_age = request.POST.get("u_age")
        u_address = request.POST.get("u_address")
        u_mobile = request.POST.get("u_mobile")
        u_gender = request.POST.get("u_gender")

        if User.objects.filter(email=u_email).exists():
            messages.error(request, "Email already in use. Please try another one.")
            return redirect('accounts:register')

        user = User.objects.create_user(
            username=u_name,
            first_name=u_fname,
            last_name=u_lname,
            email=u_email,
            password=u_password
        )

        user_profile = UserProfile(
            user=user,
            age=u_age,
            address=u_address,
            mobile=u_mobile,
            gender=u_gender
        )
        user_profile.save()

        authenticated_user = authenticate(request, username=u_name, password=u_password)
        if authenticated_user:
            auth_login(request, authenticated_user)
            messages.success(request, "Your account has been successfully created.")
            return redirect("home")

    return render(request, "accounts/register.html")


def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    profile_form = UserProfileForm(instance=user_profile)
    user_form = UserForm(instance=request.user)
    appointments = Appointment.objects.filter(user=request.user)

    bills = Bill.objects.filter(customer=request.user).prefetch_related(
        Prefetch('billitem_set', queryset=BillItem.objects.select_related('accessory'))
    ).annotate(total_item_cost=Sum('billitem__total_cost'))

    if request.method == "POST":
        if "delete_account" in request.POST:
            request.user.delete()
            auth_logout(request)
            messages.success(request, "Your account has been deleted.")
            return redirect('accounts:login')

        profile_form = UserProfileForm(request.POST, instance=user_profile)
        user_form = UserForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:user_profile')
        else:
            messages.error(request, "Error updating profile. Please check the form.")

    context = {
        'user_profile': user_profile,
        'profile_form': profile_form,
        'user_form': user_form,
        'appointments': appointments,
        'bills': bills
    }
    return render(request, 'accounts/user_profile.html', context)


def edit_profile(request):
    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        profile.age = request.POST.get('age')
        profile.address = request.POST.get('address')
        profile.mobile = request.POST.get('mobile')
        profile.gender = request.POST.get('gender')

        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']

        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:edit_profile')

    return render(request, 'accounts/edit_profile.html', {'user': user, 'profile': profile})


def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    profile_form = UserProfileForm(instance=user_profile)
    user_form = UserForm(instance=request.user)
    appointments = Appointment.objects.filter(user=request.user)

    bills = Bill.objects.filter(customer=request.user).prefetch_related(
        Prefetch('billitem_set', queryset=BillItem.objects.select_related('accessory'))
    ).annotate(total_item_cost=Sum('billitem__total_cost'))

    if request.method == "POST":
        if "delete_account" in request.POST:
            request.user.delete()
            auth_logout(request)
            messages.success(request, "Your account has been deleted.")
            return redirect('accounts:login')

        profile_form = UserProfileForm(request.POST, instance=user_profile)
        user_form = UserForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:user_profile')
        else:
            messages.error(request, "Error updating profile. Please check the form.")

    context = {
        'user_profile': user_profile,
        'profile_form': profile_form,
        'user_form': user_form,
        'appointments': appointments,
        'bills': bills
    }
    return render(request, 'accounts/user_profile.html', context)


@login_required
def logout(request):
    user = request.user
    auth_logout(request)
    messages.success(request, "Logged out Successfully!")
    return redirect('home')