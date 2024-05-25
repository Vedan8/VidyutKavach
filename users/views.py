# users/views.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import OTP, UserProfile
from .serializers import OTPRequestSerializer, OTPVerifySerializer, UserRegistrationSerializer
from datetime import timedelta

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPRequestView(APIView):
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            empId = serializer.validated_data['empId']
            password = serializer.validated_data['password']
            user = authenticate(request, empId=empId, password=password)
            profile = UserProfile.objects.get(empId=empId)
            if user is None:
                return Response({'error': 'Invalid empId or password'}, status=status.HTTP_400_BAD_REQUEST)
            
            otp, created = OTP.objects.get_or_create(user=user)
            otp.generate_otp()
            # Send OTP via email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp.otp}',
                'otpkjaef@gmail.com',  # From email address
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'OTP sent','email':profile.user.email}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerifyView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            empId = serializer.validated_data['empId']
            otp = serializer.validated_data['otp']
            try:
                profile = UserProfile.objects.get(empId=empId)
                user = profile.user
                otp = OTP.objects.get(user=user, otp=otp)
                # Check if OTP is expired (valid for 5 minutes)
                # if otp.created_at < timezone.now() - timedelta(minutes=5):
                #     return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }, status=status.HTTP_200_OK)
            except (UserProfile.DoesNotExist, OTP.DoesNotExist):
                return Response({'error': 'Invalid OTP or empId'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
