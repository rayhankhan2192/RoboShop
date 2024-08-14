from django.urls import path, include
from .views import *

from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('profile/', Profile.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
