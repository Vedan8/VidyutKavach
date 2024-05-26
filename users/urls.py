from django.urls import path
from .views import LoginView, VerifyOTPView

urlpatterns = [
    path('request-otp/', LoginView.as_view(), name='login'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
]
