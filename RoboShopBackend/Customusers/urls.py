from django.urls import path, include
from .views import *
from .email import *

from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('register/', RegisterUser.as_view()),
    path('accountVerification/', VerifyOTP.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
