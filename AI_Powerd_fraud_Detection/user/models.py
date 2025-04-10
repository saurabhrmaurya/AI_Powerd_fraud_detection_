from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)

    def __str__(self):
        return self.username


from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    aadhar = models.CharField(max_length=12, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name


import random

class OTP(models.Model):
    mobile = models.CharField(max_length=10)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))
