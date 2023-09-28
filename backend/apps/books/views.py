from django.shortcuts import render
from rest_framework import mixins, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.books.serializers import *
from apps.books.models import Book, Author
# Create your views here.


class BookView(viewsets.ViewSet):
    queryset = (Book.objects.all()
                .prefetch_related('authors', 'genres'))
    serializer_class = BookSerializerBase
    lookup_field = 'slug'
    permission_classes = (permissions.AllowAny,)

    def list(self, *args, **kwargs):
        books = (self.queryset)
        books_sl = self.serializer_class(books, many=True)
        return Response(books_sl.data)

    def retrieve(self, request, slug, *args, **kwargs):
        serializer = ShowBook(data={'slug': slug})
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        books_sl = self.serializer_class(book)
        return Response(books_sl.data)

    @action(methods=['patch'], detail=False, serializer_class=ShowBooksByYear)
    def by_year(self, request, year=None, *args, **kwargs):
        serializer = ShowBooksByYear(data=request.data)
        serializer.is_valid(raise_exception=True)
        books = serializer.save()
        books_sl = BookSerializerBase(instance=books, many=True)
        return Response(books_sl.data)

    @action(methods=['patch'], detail=False, serializer_class=ShowBooksByYears)
    def between_years(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        books = serializer.save()
        books_sl = BookSerializerBase(instance=books, many=True)
        return Response(books_sl.data)

    @action(methods=['post'], detail=False, serializer_class = AddBookSerializer)
    def add_book(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        book_sl = self.serializer_class(instance=book)
        return Response(book_sl.data)

    @action(methods=['patch'], detail=False, serializer_class=EditBookSerializer)
    def edit_book(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        book_sl = self.serializer_class(instance=book)
        return Response(book_sl.data)

    @action(methods=['delete'], detail=False, serializer_class=DeleteBookSerializer)
    def delete_book(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'book':'a book with given id was deleted successfully'})

    @action(methods=['post'], detail=False, serializer_class=AddBookAuthorSerializer)
    def add_book_author(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        book_sl = BookSerializerBase(book)
        return Response(book_sl.data)

    @action(methods=['delete'], detail=False, serializer_class=DeleteBookAuthorSerializer)
    def delete_book_author(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        book = serializer.save()
        book_sl = BookSerializerBase(book)
        return Response(book_sl.data)

