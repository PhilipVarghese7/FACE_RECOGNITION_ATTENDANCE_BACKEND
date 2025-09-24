from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),          # signup
    path("login/", TokenObtainPairView.as_view(), name="login"),         # login → JWT
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # refresh token
]
