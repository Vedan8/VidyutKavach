# users/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_otp.oath import TOTP
from django_otp.util import random_hex
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import binascii
import logging
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from dj_rest_auth.registration.serializers import VerifyEmailSerializer

logger = logging.getLogger(__name__)

class OTPVerification(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            key = binascii.unhexlify(random_hex(20))
            totp = TOTP(key=key, step=300)
            totp.time = int(totp.time / totp.step) * totp.step
            otp = totp.token()

            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            # Store the OTP and email in the session
            request.session['otp'] = otp
            request.session['otp_email'] = email

            logger.debug(f'Generated OTP: {otp} for email: {email}')

            return Response({'detail': 'OTP sent'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Error sending OTP email: {e}')
            return Response({'detail': 'Error sending OTP email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        otp = request.data.get('otp')
        email = request.data.get('email')

        if not otp:
            return Response({'detail': 'OTP is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not email:
            return Response({'detail': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        session_otp = request.session.get('otp')
        session_email = request.session.get('otp_email')

        if int(session_otp) == int(otp) and session_email == email:
            # Update user verification status
            user.is_verified = True
            user.save()
            
            return Response({'detail': 'OTP verified'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        request.session.flush()
        return Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)


class CustomConfirmEmailView(APIView):
    def get(self, request, *args, **kwargs):
        key = kwargs.get('key')
        email_confirmation = None

        try:
            email_confirmation = EmailConfirmationHMAC.from_key(key)
        except EmailConfirmation.DoesNotExist:
            try:
                email_confirmation = EmailConfirmation.objects.get(key=key)
            except EmailConfirmation.DoesNotExist:
                return Response({"detail": "Invalid key"}, status=status.HTTP_400_BAD_REQUEST)

        if email_confirmation:
            email_confirmation.confirm(request)
            return Response({"detail": "Email confirmed"}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid key"}, status=status.HTTP_400_BAD_REQUEST)