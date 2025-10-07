from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.html import mark_safe
import os, random

# ✅ Generate unique file path for uploaded profile images
def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    randomstr = ''.join(random.choice(chars) for x in range(10))
    return f'profilepic/{basefilename}_{randomstr}{file_extension}'


# ✅ USER PROFILE MODEL
class UserProfile(models.Model):
    fullname = models.CharField(max_length=150, verbose_name="Full Name")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female")],
        verbose_name="Gender"
    )
    contact_number = models.CharField(max_length=20, unique=True, verbose_name="Contact Number")
    address = models.CharField(max_length=255, blank=True, null=True)
    user_image = models.ImageField(
        upload_to=image_path,
        default='profilepic/default.png',  # ✅ match folder structure, not 'profile_pic'
        blank=True,
        null=True
    )
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # ✅ should be hashed if using Django auth

    def __str__(self):
        return f"{self.fullname} ({self.username})"

    # ✅ Display image in Django Admin
    def image_tag(self):
        if self.user_image:
            return mark_safe(
                f'<img src="{self.user_image.url}" width="120" height="120" '
                f'style="object-fit: cover; border-radius: 8px;" />'
            )
        return "-"
    image_tag.short_description = 'Profile Image'


# ✅ INVENTORY ITEM MODEL
class InventoryItem(models.Model):
    ItemID = models.AutoField(primary_key=True)
    ItemName = models.CharField(max_length=100)
    Category = models.CharField(max_length=50, null=True, blank=True)
    Quantity = models.IntegerField(default=0, null=True, blank=True)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    DateAdded = models.DateTimeField(default=timezone.now)
    Description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.ItemName} ({self.Category if self.Category else 'No Category'})"
