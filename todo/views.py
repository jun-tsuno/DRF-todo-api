from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response

from .serializers import UserSerializer, LoginSerializer, SignupSerializer

# Create your views here.
class LoginView(APIView):
  def post(self, request):
    print(request.data)
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
      username = request.data.get('username')
      password = request.data.get('password')
      user = authenticate(username=username, password=password)
      if user:
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({"token": token.key, "user": serializer.data})
      else:
        return Response({"error": "User Not Found"}, status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class SignupView(APIView):
  def post(self, request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
      email = request.data.get('email')
      password = request.data.get('password')

      if User.objects.filter(email=email).exists():
        return Response({"error": "User already exists with the email"})
      try:
        user = User.objects.create_user(username=email, email=email, password=password)
      except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

      token = Token.objects.create(user=user)
      return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)