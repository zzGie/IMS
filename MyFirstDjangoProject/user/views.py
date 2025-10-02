from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from .models import SystemUser   # ✅ make sure SystemUser is imported

def index(request):
    return render(request, "user/index.html")

def userlist(request):
    user_list = SystemUser.objects.all()
    context = {
        "user_list": user_list
    }
    return render(request, "user/userlist.html", context)

def adduser(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        contact_number = request.POST.get("contact_number")
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_image = request.FILES.get("user_image")

        try:
            user = SystemUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                contact_number=contact_number,
                username=username,
                password=make_password(password),
                user_image=user_image
            )
            user.save()
            messages.success(request, "User added successfully!")
            return redirect("userlist")
        except IntegrityError:
            messages.error(request, "Email or Username already exists.")
            return redirect("adduser")

    return render(request, "user/adduser.html")
