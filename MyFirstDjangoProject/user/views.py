from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import UserProfile
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.hashers import make_password
# Create your views here.

def index(request):
    user_list = UserProfile.objects.all()
    context = {
        'user_list': user_list
    }
    return render(request, 'user/index.html', context)


def userlist(request):
    user_list = UserProfile.objects.all()
    context = {
        'user_list': user_list
    }
    return render(request, 'user/userlist.html', context)

def adduser(request):
    if request.method == "POST":
        contact_number = request.POST.get("contact_number")
        
        # Check duplicate
        if UserProfile.objects.filter(contact_number=contact_number).exists():
            messages.error(request, "Contact number already exists. Please use another.")
            return redirect("add_user")  # or return render(request, "add_user.html")
        
        try:
            user = UserProfile(
                fullname=request.POST.get("fullname"),
                username=request.POST.get("username"),
                email=request.POST.get("email"),
                password=request.POST.get("password"),
                contact_number=contact_number,
                gender=request.POST.get("gender"),
                address=request.POST.get("address"),
                user_image=request.FILES.get("user_image"),
            )
            user.save()
            messages.success(request, "User added successfully!")
            return redirect("userlist")
        except IntegrityError:
            messages.error(request, "Error saving user. Try again.")
            return redirect("adduser")
    
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