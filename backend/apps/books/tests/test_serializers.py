from collections import OrderedDict

from django.test import TestCase
from apps.books.tests.DATA import *  # All data which test cases use
from apps.books.models import *
from apps.books.serializers import *


class BookSerializerTestCase(TestCase):
    def test_author_serializer(self):
        authors = [Author.objects.create(**author) for author in AUTHORS]
        data = AuthorSerializerBase(authors, many=True).data
        expected_data = []
        for i, author in enumerate(authors):
            author_info = {
                "id": author.id,
                "first_name": author.first_name,
                "last_name": author.last_name,
                "birth_year": author.birth_year,
                "death_year": author.death_year,
                "country": author.country,
                "slug": author.slug}
            expected_data.append(author_info)
        self.assertEqual(expected_data, data)

    def test_genre_serializer(self):
        genres = [Genre.objects.create(**genre) for genre in GENRES]
        data = GenreSerializerBase(genres, many=True).data
        expected_data = []
        for i, genre in enumerate(genres):
            genre_info = {
                "id": genre.id,
                "name": genre.name,
                "description": genre.description,
                "slug": genre.slug}
            expected_data.append(genre_info)
        self.assertEqual(expected_data, data)

    def test_book_serializer(self):
        books = [Book.objects.create(**book) for book in BOOKS]
        data = BookSerializerBase(books, many=True).data
        expected_data = []
        for i, book in enumerate(books):
            book_info = {
                "id": book.id,
                "name": book.name,
                "slug": book.slug,
                "publish_year": book.publish_year,
                "authors": [],
                "genres": [],
                "country": book.country,
                "description": book.description,
            }
            expected_data.append(book_info)
        self.assertEqual(expected_data, data)

    def test_book_serializer_with_data(self):
        genres = tuple([Genre.objects.create(**genre) for genre in GENRES])
        authors = tuple([Author.objects.create(**author) for author in AUTHORS])
        books = []
        expected_data = []
        for book_info in BOOKS:
            book = Book.objects.create(**book_info)
            book.save()
            book.authors.add(*authors)
            book.genres.add(*genres)
            books.append(book)

            book_json = {
                "id": book.id,
                "name": book.name,
                "slug": book.slug,
                "authors": AuthorSerializerBase(authors, many=True).data,
                "genres": GenreSerializerBase(genres, many=True).data,
                "publish_year": book.publish_year,
                "country": book.country,
                "description": book.description,
            }
            expected_data.append(book_json)
        data = BookSerializerBase(books, many=True).data
        # self.assertEqual(expected_data[1], data[1])
