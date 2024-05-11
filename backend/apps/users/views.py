
from rest_framework import (permissions, viewsets)

from rest_framework.decorators import action

from rest_framework.response import Response

from apps.users.models import User

from apps.users.serializers import (UserSerializerBase,
                                    UserCreateSerializer,
                                    UserChangeSerializer)

from apps.users.permisions import IsOwnerOrAdminUser

from apps.users.tasks import send_verify_email, check_verify_email


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class_dict = \
        {
            'create': UserCreateSerializer,
            'list': UserSerializerBase,
            'retrieve': UserSerializerBase,
            'update': UserChangeSerializer,
            'partial_update': UserChangeSerializer,
            'destroy': UserChangeSerializer,
        }
    permission_classes_dict = \
        {
            'list': (permissions.AllowAny,),
            'retrieve': (permissions.IsAdminUser,),
            'create': (permissions.AllowAny,),
            'update': (IsOwnerOrAdminUser,),
            'partial_update': (IsOwnerOrAdminUser,),
            'destroy': (IsOwnerOrAdminUser,),
        }

    @action(name='verify_email', methods=['get'], detail=False)
    def verify_email(self, **kwargs):
        token = kwargs.get('token')
        response_data = check_verify_email(token=token)
        return Response(data=response_data['message'],
                        status=response_data['status'],)

    def create(self, request, *args, **kwargs):
        create_response = super().create(request, *args, **kwargs)
        send_verify_email.delay(data=create_response.data)
        create_response.data['message'] = "we sent you an email to activate account"
        return create_response

    def get_serializer_class(self):
        return self.serializer_class_dict.get(self.action)

    def get_permissions(self):
        permission_classes = (permissions.AllowAny, )
        if self.action in ('update', 'destroy', 'partial_update'):
            permission_classes = (IsOwnerOrAdminUser,)
        return (permission() for permission in permission_classes)
