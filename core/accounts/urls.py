from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import signup_page, login_page

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),          # signup
    path("login/", TokenObtainPairView.as_view(), name="login"),         # login → JWT
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup-page/", signup_page, name="signup_page"),
    path("login-page/", login_page, name="login_page"),              
]
