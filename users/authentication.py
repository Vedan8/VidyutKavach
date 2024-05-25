# users/authentication.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import UserProfile

class EmpIdBackend(ModelBackend):
    def authenticate(self, request, empId=None, password=None, **kwargs):
        User = get_user_model()
        try:
            profile = UserProfile.objects.get(empId=empId)
            user = profile.user
        except UserProfile.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
