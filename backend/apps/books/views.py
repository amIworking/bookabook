from django.shortcuts import render
from rest_framework import mixins, viewsets, permissions
from rest_framework.response import Response

from apps.books.serializers import BookSerializerBase
from apps.books.models import Book, Author
# Create your views here.


class BookView(viewsets.ViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializerBase
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        books = self.serializer_class(self.queryset, many=True)
        return Response(books.data)
    
    def add_book(self, request, *args, **kwargs):
        pass
    def show_book(self, request, *args, **kwargs):
        pass

    def edit_book(self, request, *args, **kwargs):
        pass

    def delete_book(self, request, *args, **kwargs):
        pass