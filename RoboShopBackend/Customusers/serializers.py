from rest_framework import serializers
from .models import Users
from djoser.serializers import UserCreateSerializer
from .email import send_otp_via_mail
from .email import *


class UserCreateSerializers(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Users
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'phone',
        ]
    def create(self, validated_data):
        email = validated_data['email']
        user_data = {
            'first_name': validated_data.get('first_name', ''),
            'last_name': validated_data.get('last_name', ''),
            'phone': validated_data.get('phone', ''),
            'password': validated_data.get('password', ''),
        }
        otp = str(random.randint(10000, 99999))
        send_otp_via_mail(email, otp)
        #session_otp_store[email]['user_data'] = user_data
        request = self.context.get('request')
        if request:
            request.session[email] = {
            'otp': otp,
            'created_at': timezone.now().isoformat(),
            'user_data': user_data
            }
        else:
            raise ValueError("Request object is not available in serializer context")
        return validated_data
    
class VarifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    class Meta:
        model = Users
        fields = ("first_name","last_name","address","email","phone","role",)
        
    def get_role(self, instance):
        if instance.is_superuser or instance.is_staff:
            return "Admin"
        else:
            return "Customer"

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ("first_name", "last_name", "address", "email", "phone")
    
    def update(self, instance, validated_data):
        email = validated_data.get('email', instance.email)
        request = self.context.get('request')

        if not request:
            raise ValueError("Request object is not available in serializer context")

        if email != instance.email:
            # If the email has changed, send OTP and store session data
            otp = str(random.randint(10000, 99999))
            send_otp_via_mail(email, otp)
            user_data = {
                'user_id': validated_data.get('user_id', instance.id),
                'first_name': validated_data.get('first_name', instance.first_name),
                'last_name': validated_data.get('last_name', instance.last_name),
                'address': validated_data.get('address', instance.address),
                'phone': validated_data.get('phone', instance.phone),
            }
            # Store OTP and user data in the session
            request.session[email] = {
                'otp': otp,
                'created_at': timezone.now().isoformat(),
                'user_data': user_data
            }
            # Return session data to indicate that OTP has been sent
            return {
                'message': 'OTP sent to the new email address',
                'session_data': request.session[email], 
            }
        else:
            # If email hasn't changed, update the instance directly
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.address = validated_data.get('address', instance.address)
            instance.phone = validated_data.get('phone', instance.phone)
            instance.email = email  # This remains the same, but it's fine to reassign

            instance.save()
            return instance