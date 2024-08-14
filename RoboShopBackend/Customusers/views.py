from django.shortcuts import render

from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response


class Profile(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = Users.objects.get(email = request.user.email)
        except(ObjectDoesNotExist):
            return Response({'error':'User Does Not Exist'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSerializer(user, many = False, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)