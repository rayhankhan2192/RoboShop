from django.urls import path, include
from .views import *
from .email import *

from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('register/', RegisterUser.as_view(), name='user_registration'),
    path('accountVerification/', VerifyOTP.as_view(), name='user_account_verify'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfile.as_view(), name='user_profile'),
    path('logout/', LogOut.as_view(), name='user_logout'),
]
