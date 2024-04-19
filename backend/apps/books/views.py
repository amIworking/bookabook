
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author, Book, BookReview
from rest_framework import (generics, permissions,
                            viewsets, status, mixins)
from .serializers import (BookSerializerBase,
                          BookReviewSerializerBase)

from .permissions import IsOwnerOrAdminUser, AnyNotAllowed



class BookView(viewsets.ModelViewSet):
    queryset = (Book.objects.all()
                    .select_related('author'))
    serializer_class = BookSerializerBase
    lookup_field = 'slug'
    permission_classes_dict = \
        {   'list': (permissions.AllowAny,),
            'retrieve': (permissions.AllowAny,),
            'create': (permissions.IsAuthenticated,),
            'update': (permissions.IsAdminUser,),
            'partial_update': (permissions.IsAdminUser,),
            'destroy': (permissions.IsAdminUser,),
         }

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        reviews_queryset = BookReview.objects.filter(book_id=response.data['pk'])
        reviews_sr = BookReviewSerializerBase(instance=reviews_queryset, many=True)
        response.data['reviews'] = reviews_sr.data
        return response

    def get_permissions(self):
        try:
            permissions = self.permission_classes_dict[self.action]
        except KeyError:
            permissions = (AnyNotAllowed,)
        return (permission() for permission in permissions)


class BookReviewView(viewsets.ModelViewSet):
    queryset = (BookReview.objects.all()
                          .select_related('user', 'book'))
    serializer_class = BookReviewSerializerBase
    permission_classes_dict = \
        {'list': (permissions.AllowAny,),
         'retrieve': (permissions.IsAdminUser,),
         'create': (permissions.IsAuthenticated,),
         'update': (IsOwnerOrAdminUser,),
         'partial_update': (IsOwnerOrAdminUser,),
         'destroy': (IsOwnerOrAdminUser,),
         }

    def get_permissions(self):
        try:
            permissions = self.permission_classes_dict[self.action]
        except KeyError:
            permissions = (AnyNotAllowed,)
        return (permission() for permission in permissions)

