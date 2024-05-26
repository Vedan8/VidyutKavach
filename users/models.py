from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import random
import string
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, empId, email, role, password=None, **extra_fields):
        if not empId:
            raise ValueError('The Employee ID must be set')
        if not email:
            raise ValueError('The Email must be set')

        email = self.normalize_email(email)
        user = self.model(empId=empId, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, empId, email, role, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(empId, email, role, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    empId = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'empId'
    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return self.empId

    def set_otp(self):
        self.otp = ''.join(random.choices(string.digits, k=6))
        self.otp_created_at = timezone.now()
        self.save()

    def verify_otp(self, otp):
        if self.otp == otp and (timezone.now() - self.otp_created_at).seconds < 300:
            self.otp = None
            self.save()
            return True
        return False
