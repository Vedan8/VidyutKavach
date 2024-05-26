from rest_framework import serializers
from .models import CustomUser

class LoginSerializer(serializers.Serializer):
    empId = serializers.CharField()
    password = serializers.CharField()

class OTPVerifySerializer(serializers.Serializer):
    empId = serializers.CharField()
    otp = serializers.CharField()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('empId', 'email', 'role', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            empId=validated_data['empId'],
            email=validated_data['email'],
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user
