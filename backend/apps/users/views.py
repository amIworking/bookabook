from rest_framework import (generics, permissions,
                            viewsets, status, mixins)

from apps.users.models import User
from apps.users.serializers import (UserSerializerBase, UserCreateSerializer,
                               UserChangeSerializer)
from apps.users.permisions import IsOwnerOrAdminUser


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    def get_serializer_class(self):
        serializer_class = UserSerializerBase
        if self.action == 'create':
            serializer_class = UserCreateSerializer
        if self.action in ('update', 'destroy', 'partial_update'):
            serializer_class = UserChangeSerializer
        return serializer_class
    def get_permissions(self):
        permission_classes = (permissions.AllowAny, )
        if self.action in ('update', 'destroy', 'partial_update'):
            permission_classes = (IsOwnerOrAdminUser,)
        return (permission() for permission in permission_classes)





