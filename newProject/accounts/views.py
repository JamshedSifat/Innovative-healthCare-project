from django.shortcuts import render

# Create your views here.
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