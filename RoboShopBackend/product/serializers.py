from rest_framework import serializers
from .models import Product, ProductMedia, Category, Sub_category, HomePage, HomeSlide, Specialoffer


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
    
class ProductSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = (
            'category',
            'sub_category',
            'product_code',
            'after_discount',
            'color',
            'stock',
            'total_review'
        )

class HomeSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSlide
        fields = '__all__'

class SpecialofferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialoffer
        fields = '__all__'

class ProductSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','price','image','discription',)
        
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Sub_category
        fields = ["id","name","image"]

class CatagorySerializer(serializers.ModelSerializer):
    #product = ProductSerializerList(source="product_set",many=True,read_only=True)
    product = serializers.SerializerMethodField()
    sub_category = serializers.SerializerMethodField()
    def get_product(self, obj):
        categories = obj.product_set.all() 
        sub_data = Sub_category.objects.filter(category = obj)
        data = []
        if sub_data.exists():
            for i in sub_data:
                o = i.product_set.all()
                ser_data = ProductSerializerList(o,many=True,context={'request':self.context.get('request')})
                data+=ser_data.data
        
        category_serializer = ProductSerializerList(categories, many=True, context={'request':self.context.get('request')})
        data+=category_serializer.data
        return data[:7]
    class Meta:
        model = Category
        fields = ["id","name","image","product","sub_category"]
    def get_sub_category(self,instance):
        sub = Sub_category.objects.filter(category=instance)
        if sub.exists():
            ser = SubCategorySerializer(sub,many=True, context={'request':self.context.get('request')})
            return ser.data
        else:
            return None

class CatagoryListSerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ["id","name","sub_category"]
       
class HomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePage
        fields = '__all__'
    homeSlider = serializers.SerializerMethodField()
    specialoffer = serializers.SerializerMethodField()
    catagory = serializers.SerializerMethodField()
    catagoryList = serializers.SerializerMethodField()
    
    def get_homeSlider(self, obj):
        homeSlider = HomeSlide.objects.filter(isActive = True)
        homeSlider_serializer = HomeSlideSerializer(homeSlider, many = True, context={'request':self.context.get('request')})
        return homeSlider_serializer.data
    
    def get_specialoffer(self,obj):
        spacialoffer = Specialoffer.objects.filter(isactive = True)
        spacialoffer_serializer = SpecialofferSerializer(spacialoffer,many = True, context={'request':self.context.get('request')})
        return spacialoffer_serializer.data
    
    def get_catagory(self,obj):
        pass
    def get_catagoryList(self,obj ):
        pass

