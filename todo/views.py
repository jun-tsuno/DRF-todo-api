from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, LoginSerializer, SignupSerializer, TodoSerializer
from .models import CustomUser, Todo

# Create your views here.
class LoginView(APIView):
  def post(self, request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
      email = request.data.get('email')
      password = request.data.get('password')
      user = authenticate(email=email, password=password)
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
      username = request.data.get('username')
      email = request.data.get('email')
      password = request.data.get('password')
      try:
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
      except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

      token = Token.objects.create(user=user)
      return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoListView(APIView):
  authentication_classes = [SessionAuthentication, TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    todo_list = Todo.objects.filter(user=request.user)
    serializer = TodoSerializer(todo_list, many=True)
    return Response({"todo": serializer.data})