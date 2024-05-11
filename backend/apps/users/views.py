
from rest_framework import (permissions, viewsets)

from rest_framework.decorators import action

from rest_framework.response import Response

from apps.books.permissions import AnyNotAllowed
from apps.users.models import User

from apps.users.serializers import (UserSerializerBase,
                                    UserCreateSerializer,
                                    UserChangeSerializer)

from apps.users.permisions import IsOwnerOrAdminUser, IsRegistered

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
            'verify_email_again': UserSerializerBase,
        }
    permission_classes_dict = \
        {
            'list': (permissions.AllowAny,),
            'retrieve': (permissions.IsAdminUser,),
            'create': (permissions.AllowAny,),
            'update': (IsOwnerOrAdminUser,),
            'partial_update': (IsOwnerOrAdminUser,),
            'destroy': (IsOwnerOrAdminUser,),
            'verify_email_again': (permissions.AllowAny,)
        }

    @action(name='verify_email_again', methods=['post'], detail=False)
    def verify_email_again(self, request):
        email = request.data.get('email')
        if not email:
            return Response(data={"email": "Required field"}, status=400)
        user = User.objects.filter(email=email).first()
        if not user:
            return Response(data={"message": "A user with given email doesn't exist"},
                            status=400)
        if user.is_active:
            response_data = \
                {
                    "message": "Your account already has been activated",
                    "status": 400
                }
        else:
            send_verify_email.delay(email=user.email)
            response_data = \
                {
                    "message": "We sent you an email to activate account",
                    "status": 200
                }
        return Response(data={"message": response_data['message']},
                        status=response_data['status'], )

    @action(name='verify_email', methods=['get'], detail=False)
    def verify_email(self, request, **kwargs):
        response_data = check_verify_email(token=kwargs.get('token'))
        return Response(data=response_data['message'],
                        status=response_data['status'],)

    def create(self, request, *args, **kwargs):
        create_response = super().create(request, *args, **kwargs)
        send_verify_email.delay(email=create_response.data['email'])
        create_response.data['message'] = "We sent you an email to activate account"
        return create_response

    def get_serializer_class(self):
        return self.serializer_class_dict.get(self.action)

    def get_permissions(self):
        all_permissions = self.permission_classes_dict.get(self.action)
        if not all_permissions:
            all_permissions = (AnyNotAllowed,)
        return (permission() for permission in all_permissions)
