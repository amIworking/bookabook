from django.db import transaction
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author, Book, BookReview
from rest_framework import (generics, permissions,
                            viewsets, status, mixins)
from apps.books.serializers import (BookSerializerBase,
                                    BookRetrieveSerializer,
                                    BookCreateSerializer,
                                    BookChangeSerializer,
                                    AuthorSerializerBase,
                                    AuthorCreateSerializer,
                                    AuthorChangeSerializer,
                                    BookReviewSerializerBase,
                                    BookReviewCreateSerializer,
                                    BookReviewChangeSerializer,)

from apps.books.permissions import IsOwnerOrAdminUser, AnyNotAllowed


class BookView(viewsets.ModelViewSet):
    queryset = (Book.objects.all()
                    .select_related('author'))
    lookup_field = 'slug'
    permission_classes_dict = \
        {
            'list': (permissions.AllowAny,),
            'retrieve': (permissions.AllowAny,),
            'create': (permissions.IsAuthenticated,),
            'update': (IsOwnerOrAdminUser,),
            'partial_update': (IsOwnerOrAdminUser,),
            'destroy': (permissions.IsAdminUser,),
        }
    serializer_class_dict = \
        {
            'list': BookSerializerBase,
            'retrieve': BookRetrieveSerializer,
            'create': BookCreateSerializer,
            'update': BookChangeSerializer,
            'partial_update': BookChangeSerializer,
            'destroy': BookChangeSerializer,
        }

    def get_serializer_class(self):
        return self.serializer_class_dict.get(self.action)

    def get_permissions(self):
        permissions = self.permission_classes_dict.get(self.action)
        if not permissions:
            permissions = (AnyNotAllowed,)
        return (permission() for permission in permissions)


class BookReviewView(viewsets.ModelViewSet):
    queryset = (BookReview.objects.all()
                          .select_related('user', 'book'))
    permission_classes_dict = \
        {
            'list': (permissions.AllowAny,),
            'retrieve': (permissions.IsAdminUser,),
            'create': (permissions.IsAuthenticated,),
            'update': (IsOwnerOrAdminUser,),
            'partial_update': (IsOwnerOrAdminUser,),
            'destroy': (IsOwnerOrAdminUser,),
         }
    serializer_class_dict = \
        {
            'list': BookReviewSerializerBase,
            'retrieve': BookReviewSerializerBase,
            'create': BookReviewCreateSerializer,
            'update': BookReviewChangeSerializer,
            'partial_update': BookReviewChangeSerializer,
            'destroy': BookReviewChangeSerializer,
        }

    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            book_review = self.get_object()
            book = Book.objects.select_for_update().get(id=book_review.book_id)
            book.rating_sum -= book_review.rating_review
            book.rating_quantity -= 1
            book.save()
        return super().destroy(request, *args, **kwargs)



    def get_permissions(self):
        permissions = self.permission_classes_dict.get(self.action)
        if not permissions:
            permissions = (AnyNotAllowed,)
        return (permission() for permission in permissions)

    def get_serializer_class(self):
        return self.serializer_class_dict.get(self.action)


class AuthorView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    lookup_field = 'slug'
    permission_classes_dict = \
        {
            'list': (permissions.AllowAny,),
            'retrieve': (permissions.AllowAny,),
            'create': (permissions.IsAuthenticated,),
            'update': (IsOwnerOrAdminUser,),
            'partial_update': (IsOwnerOrAdminUser,),
            'destroy': (permissions.IsAdminUser,),
        }
    serializer_class_dict = \
        {
            'list': AuthorSerializerBase,
            'retrieve': AuthorSerializerBase,
            'create': AuthorCreateSerializer,
            'update': AuthorChangeSerializer,
            'partial_update': AuthorChangeSerializer,
            'destroy': AuthorChangeSerializer,
        }

    def get_serializer_class(self):
        return self.serializer_class_dict.get(self.action)

    def get_permissions(self):
        permissions = self.permission_classes_dict.get(self.action)
        if not permissions:
            permissions = (AnyNotAllowed,)
        return (permission() for permission in permissions)
