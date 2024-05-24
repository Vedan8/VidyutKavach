# users/urls.py
from django.urls import path
from .views import OTPRequestView, OTPVerifyView, UserRegistrationView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserAddressView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('request-otp/', OTPRequestView.as_view(), name='request-otp'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('address/', UserAddressView.as_view(), name='user-address'),
]
