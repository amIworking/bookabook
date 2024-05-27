from django.core.cache import cache
from rest_framework import serializers

from apps.users.exeptions import AccountAlreadyActivated, AccountDoesNotExist, \
    TokenIsInvalidOrGotInspired
from apps.users.models import User


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


class ActivateAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)

    def validate(self, attrs: dict) -> dict:
        email = attrs.get('email')
        if not email:
            raise serializers.ValidationError({'email': "Required field"})
        user = User.objects.filter(email=email).first()
        if not user:
            raise AccountDoesNotExist
        if user.is_active:
            raise AccountAlreadyActivated
        attrs['email'] = email
        return attrs


class VerifyEmailSerializer(ActivateAccountSerializer):
    token = serializers.CharField()

    def validate(self, attrs: dict) -> dict:
        email = cache.get(attrs.get('token'))
        if not email:
            raise TokenIsInvalidOrGotInspired
        attrs['email'] = email
        attrs = super().validate(attrs)
        return attrs

    def save(self, **kwargs):
        user = User.objects.get(email=self.validated_data['email'])
        user.is_active = True
        user.save()
