# users/models.py
from django.contrib.auth.models import User
from django.db import models
import random
import string
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empId = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.empId

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def generate_otp(self):
        self.otp_code = ''.join(random.choices(string.digits, k=6))
        self.created_at = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.user.userprofile.empId} - {self.otp_code}'
