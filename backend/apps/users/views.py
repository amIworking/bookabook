from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.serializers import RegisterUserSerializer, UserSerializerBase
from rest_framework import permissions, viewsets, status

User = get_user_model()

class UserView(viewsets.ViewSet):
    queryset = (User.objects.all())
    serializer_class = UserSerializerBase
    lookup_field = 'slug'
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        return self.serializer_class(self.queryset, many=True)

    @action(methods=['post'], detail=False, serializer_class=RegisterUserSerializer)
    def register(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print(user)
        return Response({
            "user": UserSerializerBase(instance=user).data,
            "message": "User Created Successfully. Now perform Login to get your token",
        }, status=status.HTTP_201_CREATED)