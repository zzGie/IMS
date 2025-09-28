from django.db import models

# Create your models here.
from datetime import datetime
from django.utils import timezone

from django.db import models

class UserProfile(models.Model):
    fullname = models.CharField(max_length=150, verbose_name="Full Name")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female")])
    contact_number = models.CharField(max_length=20 , unique=True)
    address = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # usually hashed, not plain text

    def __str__(self):
        return f"{self.fullname} {self.email}({self.username})"

