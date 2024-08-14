from rest_framework import serializers
from django.db.models import QuerySet
from .models import Users
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model, aauthenticate


class UserCreateSerializers(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Users
        fields = [
            'id', 
            'first_name', 
            'last_name',
            'email',  
            'password',
            'phone', 
            ]
    
    def create(self, validated_data):
        user = Users(
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        print(validated_data)
        return instance


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