from django.shortcuts import render

from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from .models import *
from django.http import Http404
from .email import *
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
import logging
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
        # email = request.data.get('email')
        # otp = request.data.get('otp')
        # Retrieve OTP data from session
        #otp_data = request.session.get(email)
        
        serializer = VarifyAccountSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otpInput = serializer.validated_data['otp']
            
            session_data = request.session.get(email)

            if not session_data:
                return Response({'error': 'Invalid OTP or OTP expired. Try again!'}, status=status.HTTP_400_BAD_REQUEST)
            stored_otp = session_data.get('otp')
            expiry_time = timezone.datetime.fromisoformat(session_data['created_at']) + timedelta(minutes=1)
            print(stored_otp)
            if stored_otp != otpInput:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
            if timezone.now() > expiry_time:
                return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

            # Extract user data from session
            user_data = session_data.get('user_data', {})
            
            if not user_data:
                return Response({'error': 'User data is missing'}, status=status.HTTP_400_BAD_REQUEST)

            # Create user
            user = Users(
                email=email,
                first_name=user_data.get('first_name', ''),
                last_name=user_data.get('last_name', ''),
                phone=user_data.get('phone', '')
            )
            user.set_password(user_data.get('password', ''))
            user.is_verified = True
            user.save()

            # Remove OTP data from session after successful verification
            del request.session[email]

            return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
