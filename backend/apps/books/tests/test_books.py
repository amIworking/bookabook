from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.books.models import *
from apps.books.serializers import *

from apps.books.tests.DATA import AUTHORS, GENRES, BOOKS  # All data which test cases use


class CRUDBookTestCase(APITestCase):

    def test_list_books(self):
        authors = (Author.objects.create(**author) for author in AUTHORS)
        genres = (Genre.objects.create(**genre) for genre in GENRES)
        books = []
        for book_info in BOOKS:
            book = Book.objects.create(**book_info)
            book.save()
            book.authors.add(*authors)
            book.genres.add(*genres)
            books.append(book)
        url = reverse('books-list')
        response = self.client.get(url)
        serializer = BookSerializerBase(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer, response.data)

    def test_detail_books(self):
        authors = (Author.objects.create(**author) for author in AUTHORS)
        genres = (Genre.objects.create(**genre) for genre in GENRES)
        books = []
        for book_info in BOOKS:
            book = Book.objects.create(**book_info)
            book.save()
            book.authors.add(*authors)
            book.genres.add(*genres)
            books.append(book)
        book = Book.objects.get(slug="anna-karenina")
        url = reverse('books-detail', kwargs={'slug': 'anna-karenina'})
        response = self.client.get(url)
        serializer = BookSerializerBase(book).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer, response.data)

    def test_add_book(self):
        url = reverse('books-add-book')
        response = self.client.post(url, data=BOOKS[0])
        book = Book.objects.get(slug=BOOKS[0]['slug'])
        expected_data = BookSerializerBase(book).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_edit_book(self):
        example_book = BOOKS[:][0]
        book = Book.objects.create(**example_book)
        book.save()
        example_book['id'] = book.id
        example_book['slug'] = 'changed_slug'
        url = reverse('books-edit-book')
        response = self.client.patch(url, data=example_book)
        book = Book.objects.get(slug=example_book['slug'])
        expected_data = BookSerializerBase(book).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_delete_book(self):
        url = reverse('books-delete-book')
        book_count = Book.objects.all().count()
        book = Book.objects.create(**BOOKS[0])
        book.save()
        book_info = BookSerializerBase(book).data
        response = self.client.delete(url, data=book_info)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(Book.objects.all().count(), book_count)

    def test_show_books_by_year(self):
        url = reverse('books-show-books-by-year')
        books = [Book.objects.create(**book) for book in BOOKS]
        books = (Book.objects
                 .prefetch_related('authors', 'genres')
                 .filter(publish_year=BOOKS[0]['publish_year']))
        data = {"publish_year": BOOKS[0]['publish_year']}
        response = self.client.put(url, data=data)
        expected_data = BookSerializerBase(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_show_books_by_years(self):
        url = reverse('books-show-books-by-years')
        books = [Book.objects.create(**book) for book in BOOKS]
        books = (Book.objects
                 .prefetch_related('authors', 'genres')
                 .filter(publish_year__range=(1000, 2000)))
        data = {"year1": 1000, "year2": 2000}
        response = self.client.put(url, data=data)
        expected_data = BookSerializerBase(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)
