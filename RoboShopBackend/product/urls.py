from django.urls import path, include
from .views import *

urlpatterns = [
    path('products/', AllProduct.as_view()),
    path('products/<int:pk>', getProduct.as_view()),
    path('catagory/<int:pk>/<str:flag>/', GetCatagoryProducts.as_view()),
    path('catagorylist/', CatagoryList.as_view()),
    path('home/', HomePageView.as_view()),
]
