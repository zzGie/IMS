from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe
import os, random

# ✅ Generate unique file path for uploaded profile images
def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    randomstr = ''.join(random.choice(chars) for _ in range(10))
    return f'profilepic/{basefilename}_{randomstr}{file_extension}'


# =========================
# ✅ USER PROFILE MODEL
# =========================
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('regular', 'Regular User')
    ]

    fullname = models.CharField(max_length=150, verbose_name="Full Name")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female")], verbose_name="Gender")
    contact_number = models.CharField(max_length=20, unique=True, verbose_name="Contact Number")
    address = models.CharField(max_length=255, blank=True, null=True)
    user_image = models.ImageField(upload_to=image_path, default='profilepic/default.png', blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='regular')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pending_admin = models.BooleanField(default=False)  # ✅ new field
    def __str__(self):
        return f"{self.fullname} ({self.username})"

    def image_tag(self):
        if self.user_image:
            return mark_safe(f'<img src="{self.user_image.url}" width="120" height="120" style="object-fit: cover; border-radius: 8px;" />')
        return "-"
    image_tag.short_description = 'Profile Image'

    def is_admin(self):
        return self.role == 'admin'


# =========================
# ✅ CATEGORY MODEL
# =========================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# =========================
# ✅ INVENTORY ITEM MODEL
# =========================
class InventoryItem(models.Model):
    ItemID = models.AutoField(primary_key=True)
    ItemName = models.CharField(max_length=100)
    Category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    Quantity = models.PositiveIntegerField(default=0)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Description = models.TextField(null=True, blank=True)
    DateAdded = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ItemName} ({self.Category.name if self.Category else 'No Category'})"
