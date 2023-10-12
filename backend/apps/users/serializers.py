from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


class UserSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'first_name', 'last_name', 'email']
        extra_kwargs = {
        'password': {'write_only': True},
    }

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'password', 'first_name',
                  'last_name', 'email', 'country',
                  'phone')

    def save(self):
        user = User.objects.create_user(**self.validated_data)

        return user
