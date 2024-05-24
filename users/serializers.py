# users/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Address

class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],  # Set the username to the email for simplicity
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_line1', 'address_line2', 'city']