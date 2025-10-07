<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from .models import SystemUser   # ✅ make sure SystemUser is imported
=======
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import UserProfile
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.hashers import make_password
# Create your views here.
>>>>>>> 8f89b27653e9f1ae7b64b7470d889ba28b7a0e95

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
<<<<<<< HEAD

    return render(request, "user/adduser.html")
=======
    
    return render(request, "user/adduser.html")


def edituser(request, id):
    """Update: Edit user details"""
    user = get_object_or_404(UserProfile, id=id)

    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.contact_number = request.POST.get("contact_number")
        user.gender = request.POST.get("gender")
        user.address = request.POST.get("address")
        user.username = request.POST.get("username")

        if request.POST.get("password"):
            user.password = make_password(request.POST.get("password"))

        if request.FILES.get("user_image"):
            user.user_image = request.FILES.get("user_image")

        try:
            user.save()
            messages.success(request, "✅ User updated successfully!")
            return redirect("userlist")
        except IntegrityError:
            messages.error(request, "⚠️ Email or Username already exists.")
            return redirect("edituser", id=id)

    return render(request, "user/edituser.html", {"user": user})


def deleteuser(request, id):
    """Delete: Remove user"""
    user = get_object_or_404(UserProfile, id=id)
    user.delete()
    messages.success(request, "🗑️ User deleted successfully!")
    return redirect("userlist")
>>>>>>> 8f89b27653e9f1ae7b64b7470d889ba28b7a0e95
