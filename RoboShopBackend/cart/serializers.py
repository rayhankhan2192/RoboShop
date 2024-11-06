from rest_framework import serializers
from .models import Cart, CartItem
from product.serializers import ProductSerializer

class cartItemsSerializers(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model: CartItem
        fields = "__all__"
        
class cartSerializerList(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = (
            "count",
            "price",
            "items",
        )
    def get_items(self, instance):
        cart_items = CartItem.objects.filter(cart = instance)
        serial_data = cartItemsSerializers(cart_items, many = True)
        return serial_data.data