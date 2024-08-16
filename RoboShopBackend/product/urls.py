from django.urls import path, include
from .views import *

urlpatterns = [
    path('products/', AllProduct.as_view()),
    path('products/<int:pk>/', getProduct.as_view()),
    path('category/<int:pk>/<str:flag>/', GetCatagoryProducts.as_view()),
    path('categorylist/', CatagoryList.as_view()),
]
