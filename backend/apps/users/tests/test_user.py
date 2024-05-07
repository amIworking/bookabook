from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from apps.users.models import User
from apps.users.views import UserView
class PositiveApiUserTestCase(APITestCase):
    def setUp(self):
        user_data = {'email': 'test@mail.ru',
                     'password': '123456!'}
        self.user = User.objects.create(**user_data)
        self.user_client = APIClient()
        self.user_client.force_authenticate(user=self.user)
        """
        admin_data = {'email': 'admin@mail.ru',
                      'password': '123456!'}
        self.admin = User.objects.create_superuser(**admin_data)
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin)
        """
    def test_userview_list(self):
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    def test_userview_create(self):
        user_data = {'email': 'test1@mail.ru',
                    'password': '123456!'}
        url = reverse('users-list')
        response = self.client.post(url, data=user_data)
        does_exist = User.objects.filter(email=user_data['email']).exists()
        self.assertEqual(does_exist, True)
        self.assertEqual(response.status_code, 201)

    def test_userview_retrieve(self):
        url = reverse('users-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_userview_put(self):
        data = {"email": self.user.email, "first_name": "AAAA", "last_name": "BBBB"}
        url = reverse('users-detail', args=[self.user.id])
        response = self.user_client.put(url, data=data)
        self.assertEqual(response.data['first_name'], data['first_name'])

    def test_userview_patch(self):
        data = {"last_name": "TTTTTT"}
        url = reverse('users-detail', args=[self.user.id])
        response = self.user_client.patch(url, data=data)
        self.assertEqual(response.data['last_name'], data['last_name'])

    def test_userview_destroy(self):
        user_data = {'email': 'test1@mail.ru',
                    'password': '123456!'}
        user = User.objects.create_user(**user_data)
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('users-detail', args=[user.id])
        response = client.delete(url)
        does_exist = User.objects.filter(id=user.id).exists()
        self.assertEqual(does_exist, False)
        self.assertEqual(response.status_code, 204)