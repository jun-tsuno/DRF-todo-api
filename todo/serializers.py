from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta(object):
    model = User
    fields = ['id', 'username', 'email']


class LoginSerializer(serializers.Serializer):
  username = serializers.CharField(min_length=1)
  password = serializers.CharField(min_length=1)


class SignupSerializer(serializers.Serializer):
  email = serializers.EmailField()
  password = serializers.CharField(min_length=1)
