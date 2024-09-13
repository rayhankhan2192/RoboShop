from django.db import models
from Customusers.models import Users
from product.models import Product
# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True, null=True)
    count = models.IntegerField()
    price = models.FloatField()

    def __str__(self) -> str:
        return self.user.email
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.user.email
