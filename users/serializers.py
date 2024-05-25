# users/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers

class OTPRequestSerializer(serializers.Serializer):
    empId = serializers.CharField()
    password = serializers.CharField(write_only=True)

class OTPVerifySerializer(serializers.Serializer):
    empId = serializers.CharField()
    otp_code = serializers.CharField(max_length=6)
# users/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    empId = serializers.CharField(max_length=10, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'empId']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        empId = validated_data.pop('empId')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user, empId=empId)
        return user

