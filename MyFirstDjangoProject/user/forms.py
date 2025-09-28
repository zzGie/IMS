from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['fullname', 'email', 'gender', 'contact_number', 'address', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),  # show password as dots
        }
