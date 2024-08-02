from django.urls import path, include
from .views import *

urlpatterns = [
    #path('', getProduct.as_view()),
    path('<slug:category_slug>/<slug:product_slug>/', getProduct.as_view())
]
