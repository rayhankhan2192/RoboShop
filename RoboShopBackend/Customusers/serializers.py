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

class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    class Meta:
        model = Users
        fields = (
            "first_name",
            "last_name",
            "balance",
            "address",
            "email",
            "phone",
            "role",
        )
        
    def get_role(self, instance):
        if instance.is_superuser or instance.is_staff:
            return "Admin"
        else:
            return "Customer"
        
        
    