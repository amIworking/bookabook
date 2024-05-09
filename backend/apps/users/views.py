from django.http import HttpResponseRedirect
from rest_framework import (generics, permissions,
                            viewsets, status, mixins, response)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse

from apps.users.models import User
from apps.users.serializers import (UserSerializerBase, UserCreateSerializer,
                               UserChangeSerializer)
from apps.users.permisions import IsOwnerOrAdminUser, AnyNotAllowed
from apps.users.service import send_change_email, send_verify_email



class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class_dict = \
        {   'create': UserCreateSerializer,
            'list': UserSerializerBase,
            'retrieve': UserSerializerBase,
            'confirm_email': UserCreateSerializer,
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

    # def create(self, request, *args, **kwargs):
    #     #self.action = 'confirm_registration'
    #     url = reverse(viewname='users-confirm-registration', request=request, *args,
    #                   **kwargs)
    #     print(request.auth, request.user)
    #     print(response.__dict__)
    #     return HttpResponseRedirect(redirect_to=url)
    @action(name='confirm_registration',
            methods=['get', 'post'],
            detail=False)
    def confirm_registration(self, request, *args, **kwargs):
        print(self.kwargs, kwargs, request)
        if request.method == 'teerre':
            data = {'res': "Fill code"}
        else:
            print(request.data, *args, **kwargs)
            if send_verify_email(data=request.data):
                return super().create(request, *args, **kwargs)
            else:
                return {'res': 'confirm_code incorrect'}
        return Response(data)
    @action(name='change_password',
            methods=['get', 'post'],
            detail=False)
    def change_password(self, request):
        if request.method == 'GET':
            data = {'res':"Fill your email"}
        else:
            data = send_change_email(request.data.get('email'))
        return Response(data)

    def get_serializer_class(self):
        return self.serializer_class_dict.get(self.action)
    def get_permissions(self):
        permission_classes = (permissions.AllowAny, )
        if self.action in ('update', 'destroy', 'partial_update'):
            permission_classes = (IsOwnerOrAdminUser,)
        return (permission() for permission in permission_classes)





