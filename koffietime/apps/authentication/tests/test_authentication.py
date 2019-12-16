from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status

from .base import AuthenticationTestCase
from koffietime.apps.authentication.models import User


class UserSignupTestCase(AuthenticationTestCase):
    """
    Test cases for user signup functionality.
    """

    def test_user_model(self):
        """
        Test user model.
        """
        user = self.user
        self.assertEqual(user.username, 'test1')
        self.assertTrue(user, str(self.user))
        self.assertEqual(User.get_short_name(user), 'test1')

    def test_user_signup(self):
        """
        Test user signup.
        """
        res = self.create_user
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            res.json()['message'], 'User successfully created.')

    def test_user_signup_bad_request(self):
        """
        Test user signup bad request with missing email.
        """
        res = self.client.post(
            reverse('user_signup'),
            self.create_user_blank_email_data,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_model_raises_validation_errors(self):
        """
        Test user model raises error if email is not provided.
        """
        User = get_user_model()
        with self.assertRaises(TypeError):
            self.user = User.objects.create_user(
                email=None,
                username='sammy',
                password='sammy@1')
        with self.assertRaises(TypeError):
            self.user = User.objects.create_user(
                email='sammy@sammy.com',
                username=None,
                password='sammy@1')
        with self.assertRaises(TypeError):
            self.user = User.objects.create_superuser(
                email='admin@admin.com',
                username='admin',
                password=None)

    def test_signup_email_validation(self):
        """
        Test signup raises email validation errors.
        """
        self.create_user
        res = self.client.post(
            reverse('user_signup'),
            self.create_user_data,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_username_validation(self):
        """
        Test signup raises username validation errors.
        """
        url = reverse('user_signup')
        spaced_username = self.client.post(
            url, self.create_user_spaced_username_data, format='json')
        short_username = self.client.post(
            url, self.create_user_short_username_data, format='json')
        blank_username = self.client.post(
            url, self.create_user_blank_username_data, format='json')
        self.assertEqual(spaced_username.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(short_username.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(blank_username.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_signup_password_validation(self):
        """
        Test signup raises password validation errors.
        """
        url = reverse('user_signup')
        short_password = self.client.post(
            url, self.create_user_short_password_data, format='json')
        spaced_password = self.client.post(
            url, self.create_user_spaced_password_data, format='json')
        strong_password = self.client.post(
            url, self.create_user_strong_password_data, format='json')
        self.assertEqual(short_password.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(spaced_password.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(strong_password.status_code,
                         status.HTTP_400_BAD_REQUEST)


class UserLoginTestCase(AuthenticationTestCase):
    """
    Test cases for user login functionality.
    """

    def test_user_can_login(self):
        """
        Test user login.
        """
        self.create_user
        res = self.client.post(
            reverse('user_login'),
            self.login_data,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.json()['token'])
        self.assertIsInstance(res.data['token'], str)

    def test_raise_error_if_user_credentials_are_wrong_on_login(self):
        """
        Test if API raises an error if a user provides
        wrong credentials on login.
        """
        res = self.client.post(
            reverse('user_login'),
            self.wrong_login_data,
            format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()[
                         'error'][0], 'The email or password you entered is incorrect. Please try again.')

    def test_raise_error_if_user_doesnot_exist(self):
        """
        Test if API raises an error if user does not exist.
        """
        res = self.client.post(
            reverse('user_login'),
            self.user_does_not_exist_login_data,
            format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()[
                         'error'][0], 'User does not exist.')

    def test_login_for_non_active_user(self):
        """
        Test login for non active user.
        """
        res = self.client.post(
            reverse('user_login'),
            self.inactive_user_login_data,
            format='json')
        print(res.json())
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()[
                         'error'][0], 'This user has been deactivated.')
