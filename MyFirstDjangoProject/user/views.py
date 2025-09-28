from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile
from .forms import UserProfileForm

def user_list(request):
    users = UserProfile.objects.all()
    return render(request, 'user/user_list.html', {'users': users})

def user_detail(request, pk):
    user = get_object_or_404(UserProfile, pk=pk)
    return render(request, 'user/user_detail.html', {'user': user})

def user_create(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserProfileForm()
    return render(request, 'user/user_form.html', {'form': form})