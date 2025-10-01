from django.db import models
from datetime import datetime
from django.utils import timezone
import os, random
from django.utils.html import mark_safe

now = timezone.now()

def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(10))
    return f'profilepic/{basefilename}_{randomstr}{file_extension}'

class UserProfile(models.Model):
    fullname = models.CharField(max_length=150, verbose_name="Full Name")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female")])
    contact_number = models.CharField(max_length=20 , unique=True)
    address = models.CharField(max_length=255, blank=True, null=True, unique=False)
    user_image = models.ImageField(upload_to=image_path, default='profile_pic/image.png')
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # usually hashed, not plain text

    def __str__(self):
        return f"{self.fullname} {self.email}({self.username})"

    # ✅ Make image_tag a method of the model
    def image_tag(self):
        if self.user_image:
            return mark_safe(f'<img src="{self.user_image.url}" width="100" height="100" />')
        return "-"
    
    image_tag.short_description = 'Profile Image'  # Optional: display name in admin
