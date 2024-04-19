from rest_framework import serializers

from .models import User


class UserSerializerBase(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = ['pk', 'email', 'first_name', 'last_name', 'is_staff']



class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
class UserChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'email', 'first_name', 'last_name']