from rest_framework import serializers
from django.db.models import QuerySet
from .models import Users
from djoser.serializers import UserCreateSerializer


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
            phone = validated_data['phone'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        print(validated_data)
        return instance


# class UserCreateSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = [
#             'id', 
#             'email', 
#             'first_name', 
#             'last_name', 
#             'password',
#             'phone', 
#             ]
    
#     def create(self, validated_data):
#         user = Users(
#             email = validated_data['email'],
#             first_name = validated_data['first_name'],
#             last_name = validated_data['last_name'],
#             phone = validated_data['phone'],
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
    
#     def update(self, instance, validated_data):
#         print(validated_data)
#         return instance