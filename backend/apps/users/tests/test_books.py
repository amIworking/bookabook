from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import *
from apps.users.serializers import *

from apps.books.tests.DATA import BOOKS, SetUP  # All data which test cases use


class CRUDBookTestCase(APITestCase):

    def test_registr_user(self):
        json_user = {
        "email": "test@gmail.ru",
        "first_name": "test",
        "last_name": "test",
        "password": "Simp1ePa$$word",
        "country": "USA",
        "phone": "+1 (23432)"
        }
        url = reverse('users-register')
        response = self.client.post(url, data=json_user)
        print(response.data)
        user = User.objects.get(email="test@gmail.ru")
        print(user.first_name, user.last_name, user.password, user.country, user.phone)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)


