from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient

from koffietime.apps.posts.models import Post


User = get_user_model()


class AuthenticationTestCase(APITestCase):
    """
    Base Test Cases for posts.
    """

    def setUp(self):
        # Initialize test client.
        self.client = APIClient()

        # Create admin
        self.admin = User.objects.create_superuser(
            email='admin@gmail.com',
            username='admin',
            password='admin@1')
        self.admin.save()

        # Create user.
        self.user = User.objects.create_user(
            email='test1@gmail.com',
            username='test1',
            password='test@1')
        self.user.save()

        # Create inactive user.
        self.inactive_user = User.objects.create_user(
            email='test3@gmail.com',
            username='test3',
            password='test@3')
        setattr(self.inactive_user, 'is_active', False)
        self.inactive_user.save()

        self.create_user_data = {
            'email': 'test2@gmail.com',
            'username': 'anything',
            'password': 'test@2'
        }

        self.create_user = self.client.post(
            reverse('user_signup'),
            self.create_user_data,
            format='json'
        )

        self.create_user_blank_email_data = {
            'email': '',
            'username': 'anything2',
            'password': 'test@2'
        }
        self.create_user_blank_username_data = {
            'email': 'user@email.com',
            'username': '',
            'password': 'test@2'
        }
        self.create_user_short_username_data = {
            'email': 'user@email.com',
            'username': 'user',
            'password': 'test@2'
        }
        self.create_user_spaced_username_data = {
            'email': 'user@email.com',
            'username': 'user 23',
            'password': 'test@2'
        }
        self.create_user_spaced_password_data = {
            'email': 'user@email.com',
            'username': 'user 23',
            'password': 'test@ 2'
        }
        self.create_user_strong_password_data = {
            'email': 'user@email.com',
            'username': 'user 23',
            'password': 'testone'
        }

        self.login_data = {
            'email': self.user.email,
            'password': 'test@1'
        }
        self.login_user = self.client.post(
            reverse('user_login'),
            self.login_data,
            format='json'
        )

        self.wrong_login_data = {
            'email': self.user.email,
            'password': self.user.email
        }
        self.user_does_not_exist_login_data = {
            'email': 'yusuf@yusuf.com',
            'password': 'yusuf@1'
        }
        self.blank_email_login_data = {
            'email': '',
            'password': self.user.password
        }
        self.blank_password_login_data = {
            'email': self.user.email,
            'password': ''
        }
        self.inactive_user_login_data = {
            'email': self.inactive_user.email,
            'password': 'test@3'
        }
