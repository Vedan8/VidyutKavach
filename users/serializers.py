# users/serializers.py

from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        return data
