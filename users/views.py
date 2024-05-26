import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login as auth_login
from .models import CustomUser
from .serializers import LoginSerializer, OTPVerifySerializer, UserRegistrationSerializer

logger = logging.getLogger(__name__)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        empId = serializer.validated_data['empId']
        password = serializer.validated_data['password']

        logger.debug(f"Attempting to authenticate user with empId: {empId}")

        user = authenticate(request, username=empId, password=password)
        if user is not None:
            if user.is_active:
                logger.debug(f"User {empId} authenticated successfully")
                # Generate and send OTP
                user.set_otp()
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {user.otp}',
                    'from@example.com',
                    [user.email],  # Send the email to the user's registered email address
                    fail_silently=False,
                )
                return Response({"message": "OTP sent to email."}, status=status.HTTP_200_OK)
            else:
                logger.debug(f"User {empId} is deactivated")
                return Response({"error": "User account is deactivated."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.debug(f"Invalid credentials for user with empId: {empId}")
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        empId = serializer.validated_data['empId']
        otp = serializer.validated_data['otp']

        logger.debug(f"Verifying OTP for empId: {empId}, provided OTP: {otp}")

        try:
            user = CustomUser.objects.get(empId=empId)
        except CustomUser.DoesNotExist:
            logger.debug(f"User with empId {empId} does not exist.")
            return Response({"error": "User with this empId does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if user.verify_otp(otp):
            auth_login(request, user)
            logger.debug(f"OTP verification successful for empId {empId}")
            return Response({"message": "OTP verified and user logged in."}, status=status.HTTP_200_OK)
        else:
            logger.debug(f"Invalid or expired OTP for empId {empId}")
            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)