from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from apps.users.models import User
from apps.books.models import Author, BookReview, Book
from apps.users.views import UserView
class PositiveApiBookTestCase(APITestCase):
    def setUp(self):
        user_data = {'email': 'test@mail.ru',
                     'password': '123456!'}
        self.user = User.objects.create(**user_data)
        self.user_client = APIClient()
        self.user_client.force_authenticate(user=self.user)

        admin_data = {'email': 'admin@mail.ru',
                      'password': '123456!'}
        self.admin = User.objects.create_superuser(**admin_data)
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin)

        author_data = {"first_name": "Stephen",
                       "last_name": 'King',
                       "birth_date": "1947-09-21",
                       "slug": "stephen-king"}
        self.author = Author.objects.create(**author_data)

        book_data = {"title": "The Talisman",
                     "slug": "the-talisman",
                     "genre": "novel",
                     "writing_date": "1984-01-01"}
        self.book = Book.objects.create(author_id=self.author.id,
                                        user_id=self.user.id, **book_data)

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


    def test_book_put(self):
        new_book_data = {"slug": "the-talisman",
                         "genre": "horror",
                        "writing_date": "2001-01-01"
                     }
        url = reverse('books-detail', [self.book.slug])
        response = self.user_client.put(url, data=new_book_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['genre'], new_book_data['genre'])


    def test_book_patch(self):
        new_book_data = {"genre": "fiction"}
        url = reverse('books-detail', [self.book.slug])
        response = self.user_client.patch(url, data=new_book_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['genre'], new_book_data['genre'])


    def test_book_destroy(self):
        book_data = {"title": "The Diary of Ellen Rimbauer: My Life at Rose Red",
                     "slug": "the-diary-of-ellen-rimbauer-my-life-at-rose-red",
                     "genre": "horror",
                     "writing_date": "2001-01-01",
                     "author_id": self.author.id,
                     "user_id": self.user.id}
        book = Book.objects.create(**book_data)
        url = reverse('books-detail', args=[book.slug])
        response = self.admin_client.delete(url)
        does_exist = Book.objects.filter(slug=book_data['slug']).exists()
        self.assertEqual(does_exist, False)
        self.assertEqual(response.status_code, 204)