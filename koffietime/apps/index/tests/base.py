from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient


User = get_user_model()


class BaseTestCase(APITestCase):
    """
    Base Test Cases for index.
    """

    def setUp(self):
        # Initialize test client.
        self.client = APIClient()
        # Create user.
        self.user = User.objects.create_user(
            email='test1@gmail.com',
            username='test1',
            password='test@1'
        )
        self.user.save()
        self.login_data = {
            'email': self.user.email,
            'password': 'test@1'
        }
        self.login = reverse('user_login')
        # Login user
        self.login_response = self.client.post(
            self.login,
            self.login_data,
            format='json'
        )
        auth_token = self.login_response.json()['token']
        self.auth_header = 'Bearer {}'.format(auth_token)
