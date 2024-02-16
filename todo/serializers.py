from rest_framework import serializers

from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
  class Meta(object):
    model = CustomUser
    fields = ['id', 'username', 'email']


class LoginSerializer(serializers.Serializer):
  email = serializers.EmailField()
  password = serializers.CharField(min_length=1)


class SignupSerializer(serializers.Serializer):
  username = serializers.CharField(max_length=10)
  email = serializers.EmailField()
  password = serializers.CharField(min_length=1)
