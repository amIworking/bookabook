from django.utils.text import slugify
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from apps.users.models import User
from apps.books.models import Author, Book

import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    email = factory.Sequence(lambda n: 'user%d@gmail.com' % n)
    password = '123456!'

    @staticmethod
    def get_auth_client(user):
        user_client = APIClient()
        user_client.force_authenticate(user=user)
        return user_client


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book
    title = factory.Sequence(lambda i: 'Test_%d' % i)
    slug = slugify(title)
    genre = "novel"

class ApiBookTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user_client = UserFactory.get_auth_client(user=self.user)

        self.other_user = UserFactory()
        self.other_user_client = UserFactory.get_auth_client(user=self.other_user)

        self.admin = User.objects.create_superuser(email='admin@mail.ru',
                                                   password='123456!')
        self.admin_client = UserFactory.get_auth_client(user=self.admin)

        author_data = {"first_name": "Stephen",
                       "last_name": 'King',
                       "birth_date": "1947-09-21",
                       "slug": "stephen-king"}
        self.author = Author.objects.create(**author_data)

        self.book = BookFactory(author_id=self.author.id,
                                user_id=self.user.id)


    def test_book_list(self):
        url = reverse('books-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_book_retrieve(self):
        url = reverse('books-detail', args=[self.book.slug])
        response = self.client.get(url)
        self.assertEqual(response.data['title'], self.book.title)
        self.assertEqual(response.status_code, 200)

    def test_book_create(self):
        book_data = {"title": "Black House",
                     "slug": "black-house",
                     "genre": "horror",
                     "writing_date": "2001-01-01",
                     "author": self.author.id,
                     "user": self.user.id}
        url = reverse('books-list')
        response = self.user_client.post(url, data=book_data)
        does_exist = Book.objects.filter(slug=book_data['slug']).exists()
        self.assertEqual(does_exist, True)
        self.assertEqual(response.status_code, 201)

    def test_not_auth_user_not_book_create(self):

        book_data = {"title": "Black House",
                     "slug": "black-house",
                     "genre": "horror",
                     "writing_date": "2001-01-01",
                     "author": self.author.id,
                     "user": self.user.id}
        url = reverse('books-list')
        response = self.client.post(url, data=book_data)
        does_exist = Book.objects.filter(slug=book_data['slug']).exists()
        self.assertEqual(does_exist, False)
        self.assertEqual(response.status_code, 401)

    def test_book_put(self):
        new_book_data = {
                        "slug": "the-talisman",
                        "genre": "horror",
                        "writing_date": "2001-01-01"
                        }
        url = reverse('books-detail', [self.book.slug])
        response = self.user_client.put(url, data=new_book_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['genre'], new_book_data['genre'])

    def test_not_auth_user_not_book_put(self):
        new_book_data = {
                        "slug": "the-talisman",
                        "genre": "horror",
                        "writing_date": "2001-01-01"
                        }
        url = reverse('books-detail', [self.book.slug])
        response = self.client.patch(url, data=new_book_data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('genre'), None)

    def test_not_owner_not_book_put(self):
        new_book_data = {
                        "slug": "the-talisman",
                        "genre": "horror",
                        "writing_date": "2001-01-01"
                        }
        url = reverse('books-detail', [self.book.slug])
        response = self.other_user_client.patch(url, data=new_book_data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data.get('genre'), None)

    def test_admin_user_book_put(self):
        new_book_data = {
                        "slug": "the-talisman",
                        "genre": "horror",
                        "writing_date": "2001-01-01"
                        }
        url = reverse('books-detail', [self.book.slug])
        response = self.admin_client.patch(url, data=new_book_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['genre'], new_book_data['genre'])

    def test_book_patch(self):
        new_book_data = {"genre": "fiction"}
        url = reverse('books-detail', [self.book.slug])
        response = self.user_client.patch(url, data=new_book_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['genre'], new_book_data['genre'])

    def test_not_auth_user_not_book_patch(self):
        new_book_data = {"genre": "fiction"}
        url = reverse('books-detail', [self.book.slug])
        response = self.client.patch(url, data=new_book_data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('genre'), None)

    def test_not_owner_not_book_patch(self):
        new_book_data = {"genre": "fiction"}
        url = reverse('books-detail', [self.book.slug])
        response = self.other_user_client.patch(url, data=new_book_data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data.get('genre'), None)

    def test_admin_user_book_patch(self):
        new_book_data = {"genre": "fiction"}
        url = reverse('books-detail', [self.book.slug])
        response = self.admin_client.patch(url, data=new_book_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['genre'], new_book_data['genre'])

    def test_admin_book_destroy(self):
        book_data = {
                     "title": "The Diary of Ellen Rimbauer: My Life at Rose Red",
                     "slug": "the-diary-of-ellen-rimbauer-my-life-at-rose-red",
                     "genre": "horror",
                     "writing_date": "2001-01-01",
                     "author_id": self.author.id,
                     "user_id": self.user.id
                    }
        book = Book.objects.create(**book_data)
        url = reverse('books-detail', args=[book.slug])
        response = self.admin_client.delete(url)
        does_exist = Book.objects.filter(slug=book_data['slug']).exists()
        self.assertEqual(does_exist, False)
        self.assertEqual(response.status_code, 204)

    def test_owner_book_not_destroy(self):
        book_data = {
                     "title": "The Diary of Ellen Rimbauer: My Life at Rose Red",
                     "slug": "the-diary-of-ellen-rimbauer-my-life-at-rose-red",
                     "genre": "horror",
                     "writing_date": "2001-01-01",
                     "author_id": self.author.id,
                     "user_id": self.user.id
                    }
        book = Book.objects.create(**book_data)
        url = reverse('books-detail', args=[book.slug])
        response = self.user_client.delete(url)
        does_exist = Book.objects.filter(slug=book_data['slug']).exists()
        self.assertEqual(does_exist, True)
        self.assertEqual(response.status_code, 403)

    def test_not_auth_user_book_not_destroy(self):
        book_data = {
                     "title": "The Diary of Ellen Rimbauer: My Life at Rose Red",
                     "slug": "the-diary-of-ellen-rimbauer-my-life-at-rose-red",
                     "genre": "horror",
                     "writing_date": "2001-01-01",
                     "author_id": self.author.id,
                     "user_id": self.user.id
                    }
        book = Book.objects.create(**book_data)
        url = reverse('books-detail', args=[book.slug])
        response = self.client.delete(url)
        does_exist = Book.objects.filter(slug=book_data['slug']).exists()
        self.assertEqual(does_exist, True)
        self.assertEqual(response.status_code, 401)
