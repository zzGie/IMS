from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserProfile
from django.db import IntegrityError
from django.contrib import messages
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