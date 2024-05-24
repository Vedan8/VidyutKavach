# users/models.py
from django.contrib.auth.models import User
from django.db import models
import random
import string

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def generate_otp(self):
        self.otp_code = ''.join(random.choices(string.digits, k=6))
        self.save()

    def __str__(self):
        return f'{self.user.email} - {self.otp_code}'
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
