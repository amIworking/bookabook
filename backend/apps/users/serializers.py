from rest_framework import serializers

from apps.users.models import User, UserManager


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserSerializerBase(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = ['pk', 'email', 'first_name', 'last_name', 'is_staff']


class UserCreateSerializer(UserSerializerBase):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

    def save(self, **kwargs):

        email = self.validated_data['email']
        password = self.validated_data['password']
        user = User(email=email)
        user.set_password(password)
        user.save()
        return user
class UserChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'email', 'first_name', 'last_name']

