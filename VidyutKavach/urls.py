"""
URL configuration for VidyutKavach project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import OTPVerification, CustomLoginView, LogoutView ,CustomConfirmEmailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/otp/', OTPVerification.as_view(), name='otp-verification'),
    path('api/auth/login/', CustomLoginView.as_view(), name='custom-login'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('allauth.urls')),
    path('confirm-email/<str:key>/', CustomConfirmEmailView.as_view(), name='confirm_email'),
]