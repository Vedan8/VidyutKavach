from rest_framework import serializers
from .models import CustomUser

class LoginSerializer(serializers.Serializer):
    empId = serializers.CharField()
    password = serializers.CharField()

class OTPVerifySerializer(serializers.Serializer):
    empId = serializers.CharField()
    otp = serializers.CharField()
