from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer

# Signup API
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def signup_page(request):
    return render(request, "signup.html")

def login_page(request):
    return render(request, "login.html")

def home_page(request):
    return render(request, "index.html")