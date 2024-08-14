from django.shortcuts import render

from .models import Product, HomePage, Category, Sub_category
from .serializers import ProductSerializer, HomePageSerializer, ProductSerializerList, CatagorySerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework.generics import ListAPIView


class getProduct(APIView):
    def get(self,request,pk,format = None):
        try:
            product = Product.objects.get(id = pk)
        except:
            return Response({'error':'Product Not Found!'},status=status.HTTP_404_NOT_FOUND)
        ser = ProductSerializer(product,many=False,context={'request':request})
        return Response(ser.data,status=status.HTTP_200_OK)
    
class AllProduct(APIView):
    def get(self, request, format = None):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class HomePageView(APIView):
    def get(self, request, format=None):
        key = request.query_params.get('key')
        if not key:
            return Response({'error': 'Key is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            homepage = HomePage.objects.get(key=key)
        except HomePage.DoesNotExist:
            return Response({'error': 'Give us valid homepage key'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = HomePageSerializer(homepage, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class CatagoryList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CatagorySerializer  
    
class GetCatagoryProducts(APIView):
    def get(self, request, pk, flag):
        if flag == "category":
            try:
                category = Category.objects.get(id = pk)
            except:
                return Response({"error":"You Give a Unvalid Category Id"},status=status.HTTP_404_NOT_FOUND)
            category_product = category.product_set.all()
            serializer = ProductSerializerList(category_product, many = True, context={'request': request})
            return Response(serializer.data)
            
        elif flag == "subcategory":
            try:
                sub_category = Sub_category.objects.get(id=pk)
            except:
                return Response({"error":"Please Give an valid Subcategory id"},status=status.HTTP_404_NOT_FOUND)
            subCategory_product = sub_category.product_set.all()
            serializer = ProductSerializerList(subCategory_product,many = True,context={'request':request})
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({"error":"You Miss valid Flag :)"},status=status.HTTP_406_NOT_ACCEPTABLE)