from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

class GetCartItems(APIView):
    
    def get(self, request):
        # # Check if the user is authenticated
        # if not request.user.is_authenticated:
        #     return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            cart = Cart.objects.get(user = request.user)
        except:
            cart = Cart(user = request.user, count = 0, price = 0)
            cart.save()
        cart_seril = cartSerializerList(cart, context = {'request': request})
        return Response(cart_seril.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            cart = Cart.objects.get(user = request.user)
        except:
            cart = Cart(user = request.user, count = 0, price = 0)
            cart.save()
        data = request.data
        if 'product' not in data:
            return Response({'error': 'Select Product Please!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if 'quantity' not in data:
            return Response({'error': 'Enter product quantity!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        product = Product.objects.get(id = data["product"])
        
        cart_items_data = CartItem.objects.filter(cart = cart, product = product)
        if cart_items_data.exists():
            cart_item = cart_items_data.first()
            cart_item.quantity += data["quantity"]
            cart_item.save()
            
            cart.price += (product.price * data["quantity"])
            cart.save()
            seril = cartSerializerList(cart, context = {'request': request})
            return Response(seril.data, status=status.HTTP_201_CREATED)
        cart.count += 1
        cart.price += (product.price * data["quantity"])
        cart.save()
        cart_item = CartItem(product = product, quantity = data["quantity"], cart = cart)
        cart_item.save()
        seril = cartSerializerList(cart, context = {'request': request})
        return Response(seril.data, status=status.HTTP_201_CREATED)
