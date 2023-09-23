from django.shortcuts import render
from rest_framework import mixins, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.books.serializers import *
from apps.books.models import Book, Author
# Create your views here.


class BookView(viewsets.ViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializerBase
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        books = (self.queryset
                 .prefetch_related('authors', 'genres'))
        books_sl = self.serializer_class(books, many=True)
        return Response(books_sl.data)

    @action(methods=['get'], detail=False, serializer_class=ShowBook)
    def show_book(self, request, *args, **kwargs):
        pre_book = self.serializer_class(data=request.data)
        pre_book.is_valid(raise_exception=True)
        book = (self.queryset
                 .prefetch_related('authors', 'genres')
                 .get(**pre_book.validated_data))
        book_sl = BookSerializerBase(book)
        return Response(book_sl.data)
    @action(methods=['get'], detail=False, serializer_class=ShowBooksByYear)
    def show_books_by_year(self, request, *args, **kwargs):
        pre_books = self.serializer_class(data=request.data)
        pre_books.is_valid(raise_exception=True)
        books = (self.queryset
                .prefetch_related('authors', 'genres')
                .filter(**pre_books.validated_data))
        books_sl = BookSerializerBase(books, many=True)
        return Response(books_sl.data)

    @action(methods=['get'], detail=False, serializer_class=ShowBooksByYears)
    def show_books_by_years(self, request, *args, **kwargs):
        pre_books = self.serializer_class(data=request.data)
        pre_books.is_valid(raise_exception=True)
        d = pre_books.validated_data
        books = (Book.objects
                 .filter(publish_year__range=(d['year1'], d['year2']))
                 .prefetch_related('authors', 'genres'))
        books_sl = BookSerializerBase(books, many=True)
        return Response(books_sl.data)

    @action(methods=['post'], detail=False)
    def add_book(self, request, *args, **kwargs):
        pass

    def edit_book(self, request, *args, **kwargs):
        pass

    def delete_book(self, request, *args, **kwargs):
        pass

    def get_serializer(self, *args, serializer_class=None, request=None, **kwargs):
        """
        Return instance of serializer with a request in context.
        """
        serializer_class = serializer_class or self.serializer_class
        if "context" not in kwargs:
            request = request or getattr(self, "request", None)
            assert request, "self.request is not set and is not passed in kwargs"
            kwargs["context"] = {"request": request}
        return serializer_class(**kwargs)