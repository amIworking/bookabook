from rest_framework import (generics, permissions,
                            viewsets, status, mixins)

from .models import User
from .serializers import UserSerializer


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

