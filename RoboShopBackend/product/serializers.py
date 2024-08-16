from rest_framework import serializers
from .models import Product, ProductMedia, Category, Sub_category


class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'image',
            'discription',
            'media',
        )
    def get_media(self,instance):
        obj = ProductMedia.objects.filter(product = instance)
        ser = ProductMediaSerializer(obj,many=True, context={'request':self.context.get('request')})
        return ser.data
    
class ProductSerializerList(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    sub_category_name = serializers.SerializerMethodField()
    class Meta:
        model = Product
        exclude = (
            'category',
            'sub_category',
            'product_code',
            'after_discount',
            'color',
            'stock',
            'total_review',
        )
    def get_category_name(self, obj):
        return [category.name for category in obj.category.all()]
    
    def get_sub_category_name(self, obj):
        return [sub_category.name for sub_category in obj.sub_category.all()]


class ProductSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','price','image','discription',)
        
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Sub_category
        fields = ["id","name","image"]


class CatagorySerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    sub_category = serializers.SerializerMethodField()

    def get_product(self, obj):
        # Use a set to store unique product IDs
        product_ids = set()
        data = []

        # Get products directly related to the category
        categories = obj.product_set.all()
        category_serializer = ProductSerializerList(categories, many=True, context={'request': self.context.get('request')})
        
        for product in category_serializer.data:
            if product['id'] not in product_ids:
                data.append(product)
                product_ids.add(product['id'])

        #Get products related to subcategories of the category
        sub_data = Sub_category.objects.filter(category=obj)
        if sub_data.exists():
            for sub_category in sub_data:
                sub_products = sub_category.product_set.all()
                sub_product_serializer = ProductSerializerList(sub_products, many=True, context={'request': self.context.get('request')})
                
                for product in sub_product_serializer.data:
                    if product['id'] not in product_ids:
                        data.append(product)
                        product_ids.add(product['id'])

        # Return only the first 7 products
        return data[:7]

    def get_sub_category(self, instance):
        sub = Sub_category.objects.filter(category=instance)
        if sub.exists():
            ser = SubCategorySerializer(sub, many=True, context={'request': self.context.get('request')})
            return ser.data
        else:
            return None

    class Meta:
        model = Category
        fields = ["id", "name", "image", "product", "sub_category"]

class CatagoryListSerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ["id","name","sub_category"]
    
