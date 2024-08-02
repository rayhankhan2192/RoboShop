from django.shortcuts import render

from .models import Product
from .serializers import ProductSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404


class getProduct(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except:
            return Http404
    
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)