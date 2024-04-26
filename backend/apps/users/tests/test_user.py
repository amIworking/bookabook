from django.test import TestCase
from apps.users.views import UserView
class UserTestCase(TestCase):

    def test_user_creation(self):
        user_data = {'email': 'test@mail.ru',
                 'password': '123456'}
        #self.client =
