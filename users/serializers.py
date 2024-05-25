# users/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers

class OTPRequestSerializer(serializers.Serializer):
    empId = serializers.CharField()
    password = serializers.CharField(write_only=True)

class OTPVerifySerializer(serializers.Serializer):
    empId = serializers.CharField()
    otp = serializers.CharField(max_length=6)
# users/serializers.py
from .models import UserProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    empId = serializers.CharField(max_length=10, write_only=True)
    email=serializers.EmailField()
    role=serializers.CharField()
    class Meta:
        model = User
        fields = ['username', 'password', 'empId','email','role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        empId = validated_data.pop('empId')
        email=validated_data.get('email')
        role=validated_data.get('role')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            role=validated_data['role']
        )
        UserProfile.objects.create(user=user, empId=empId,email=email,role=role)
        return user

