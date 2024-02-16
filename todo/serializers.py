from rest_framework import serializers

from .models import CustomUser, Todo

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


class TodoSerializer(serializers.ModelSerializer):
  status_display = serializers.SerializerMethodField()

  class Meta(object):
    model = Todo
    fields = ['id', 'title', 'status_display']

  def get_status_display(self, obj):
    return obj.get_status_display()


class TodoWriteSerializer(serializers.ModelSerializer):
  class Meta():
    model = Todo
    fields = ['title', 'status']