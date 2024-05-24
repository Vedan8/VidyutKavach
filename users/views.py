# users/views.py
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import OTP
from .serializers import OTPRequestSerializer, OTPVerifySerializer, UserRegistrationSerializer
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from .models import Address
from .serializers import AddressSerializer

# users/views.py
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import OTP
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
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            otp, created = OTP.objects.get_or_create(user=user)
            otp.generate_otp()
            # Send OTP via email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp.otp_code}',
                'from@example.com',  # From email address
                [email],
                fail_silently=False,
            )
            return Response({'message': 'OTP sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerifyView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            try:
                user = User.objects.get(email=email)
                otp = OTP.objects.get(user=user, otp_code=otp_code)

                current_time = timezone.now()
                print(f"Current time: {current_time}")
                print(f"OTP created_at: {otp.created_at}")
                print(f"Difference: {current_time - otp.created_at}")

                # Check if OTP is expired (valid for 5 minutes)
                # if otp.created_at < timezone.now() - timedelta(minutes=5):
                #     return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            except (User.DoesNotExist, OTP.DoesNotExist):
                return Response({'error': 'Invalid OTP or user'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        address = Address.objects.filter(user=user).first()
        if address:
            serializer = AddressSerializer(address)
            return Response(serializer.data)
        else:
            return Response({'message': 'No address found for the user'}, status=status.HTTP_404_NOT_FOUND)