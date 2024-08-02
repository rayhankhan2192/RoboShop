from rest_framework import serializers
from .models import Product, ProductMedia


class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'
    def get_media(self,instance):
        obj = ProductMedia.objects.filter(product = instance)
        ser = ProductMediaSerializer(obj,many=True, context={'request':self.context.get('request')})
        return ser.data