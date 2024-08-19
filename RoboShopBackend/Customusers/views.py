from django.shortcuts import render

from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import aauthenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from .models import *
from django.http import Http404
from .email import *
from django.contrib.auth import get_user_model
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
User = get_user_model()

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserCreateSerializers(data=request.data, context={'request': request})
        if serializer.is_valid():
            validated_data = serializer.save()
            return Response({"detail": "OTP sent to email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTP(APIView):
    def post(self, request):
        serializer = VarifyAccountSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otpInput = serializer.validated_data['otp']
            
            session_data = request.session.get(email)

            if not session_data:
                return Response({'error': 'Invalid OTP or OTP expired. Try again!'}, status=status.HTTP_400_BAD_REQUEST)

            stored_otp = session_data.get('otp')
            expiry_time = timezone.datetime.fromisoformat(session_data['created_at']) + timedelta(minutes=1)

            if stored_otp != otpInput:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
            if timezone.now() > expiry_time:
                return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

            # Extract user data from session
            user_data = session_data.get('user_data', {})

            if not user_data:
                return Response({'error': 'User data is missing'}, status=status.HTTP_400_BAD_REQUEST)

            # Determine if this is a new user or an existing user update
            user_id = user_data.get('user_id')  # Assume you pass user_id in session if updating

            if user_id:
                # Update the existing user
                user = Users.objects.get(id=user_id)
                user.first_name = user_data.get('first_name', user.first_name)
                user.last_name = user_data.get('last_name', user.last_name)
                user.phone = user_data.get('phone', user.phone)
                user.address = user_data.get('address', user.address)
                user.email = email  # Assuming you verified the new email via OTP
            else:
                # Create a new user
                user = Users(
                    email=email,
                    first_name=user_data.get('first_name', ''),
                    last_name=user_data.get('last_name', ''),
                    phone=user_data.get('phone', ''),
                    address=user_data.get('address', '')
                )
                user.set_password(user_data.get('password', ''))
                user.is_verified = True

            # Save the user (either new or updated)
            user.save()

            # Remove OTP data from session after successful verification
            del request.session[email]

            if user_id:
                return Response({'success': 'Updated successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfile(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            #user = request.user
            user = User.objects.get(email=request.user.email)
            serializer = ProfileSerializer(user)
            return Response(serializer.data)
        except:
            return Response({"detail": "Something Went Wrong!"}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        try:
            user = User.objects.get(email=request.user.email)
            serializer = ProfileUpdateSerializer(user,data=request.data, partial=True,context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"detail": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": "An OTP sent to your new Email!!"}, status=status.HTTP_400_BAD_REQUEST)

class LogOut(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response({"detail": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)