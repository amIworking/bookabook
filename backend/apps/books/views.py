from django.shortcuts import render
from rest_framework import mixins, viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.books.serializers import *
from apps.books.models import Book, Author
# Create your views here.

class CustomViewPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page_size'
    max_page_size = 10000

class BookView(viewsets.ViewSet):
    queryset = (Book.objects.all()
                .prefetch_related('authors', 'genres'))
    serializer_class = BookSerializerBase
    lookup_field = 'slug'
    pagination_class = CustomViewPagination
    permission_classes = (permissions.AllowAny,)

    def list(self, *args, **kwargs):
        books = (self.queryset)
        books_sl = self.serializer_class(books, many=True)
        return Response(books_sl.data)

    def retrieve(self, request, slug, *args, **kwargs):
        serializer = ShowBookSerializer(data={'slug': slug})
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


    @action(methods=['post'], detail=False, serializer_class=AddBookSerializer)
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
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        book_sl = BookSerializerBase(book)
        return Response(book_sl.data)

    @action(methods=['delete'], detail=False, serializer_class=DeleteBookAuthorSerializer)
    def delete_book_author(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        book = serializer.save()
        book_sl = BookSerializerBase(book)
        return Response(book_sl.data)

    @action(methods=['post'], detail=False, serializer_class=AddBookGenreSerializer)
    def add_book_genre(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        book_sl = BookSerializerBase(book)
        return Response(book_sl.data)

    @action(methods=['delete'], detail=False, serializer_class=DeleteBookGenreSerializer)
    def delete_book_genre(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        book = serializer.save()
        book_sl = BookSerializerBase(book)
        return Response(book_sl.data)

class AuthorView(viewsets.ViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializerBase
    lookup_field = 'slug'
    pagination_class = CustomViewPagination
    permission_classes = (permissions.AllowAny,)

    def list(self, *args, **kwargs):
        return Response(self.serializer_class(self.queryset, many=True).data)

    def retrieve(self, request, slug, *args, **kwargs):
        serializer = ShowAuthorSerializer(data={'slug': slug})
        serializer.is_valid(raise_exception=True)
        author = serializer.save()
        return Response(self.serializer_class(author).data)

    @action(methods=['post'], detail=False, serializer_class=AddAuthorSerializer)
    def add_author(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = serializer.save()
        return Response(self.serializer_class(instance=author).data)

    @action(methods=['patch'], detail=False, serializer_class=EditAuthorSerializer)
    def edit_author(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = serializer.save()
        return Response(self.serializer_class(instance=author).data)

    @action(methods=['delete'], detail=False, serializer_class=DeleteAuthorSerializer)
    def delete_author(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'author': 'an author with given id was deleted successfully'})


class GenreView(viewsets.ViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializerBase
    lookup_field = 'slug'
    pagination_class = CustomViewPagination
    permission_classes = (permissions.AllowAny,)

    def list(self, *args, **kwargs):
        return Response(self.serializer_class(self.queryset, many=True).data)

    def retrieve(self, request, slug, *args, **kwargs):
        serializer = ShowGenreSerializer(data={'slug': slug})
        serializer.is_valid(raise_exception=True)
        genre = serializer.save()
        return Response(self.serializer_class(genre).data)

    @action(methods=['post'], detail=False, serializer_class=AddGenreSerializer)
    def add_author(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        genre = serializer.save()
        return Response(self.serializer_class(instance=genre).data)

    @action(methods=['patch'], detail=False, serializer_class=EditGenreSerializer)
    def edit_genre(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        genre = serializer.save()
        return Response(self.serializer_class(instance=genre).data)

    @action(methods=['delete'], detail=False, serializer_class=DeleteGenreSerializer)
    def delete_genre(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'genre': 'a genre with given id was deleted successfully'})