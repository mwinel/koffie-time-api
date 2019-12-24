from django.urls import reverse

from rest_framework import status

from .base import BaseTestCase


class ProfilesCrudTestCase(BaseTestCase):
    """
    Test cases for profiles functionality.
    """

    def test_get_user_profiles(self):
        """
        Test get all user profiles.
        """
        res = self.client.get(
            reverse('retrieve_profiles'),
            HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_user_profile(self):
        """
        Test get user profile.
        """
        res = self.client.get(
            reverse('retrieve_profile', kwargs={'username': 'test1'}),
            HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_user_profile_which_does_not_exist(self):
        """
        Test get user profile which does not exist.
        """
        res = self.client.get(
            reverse('retrieve_profile', kwargs={'username': 'test1000'}),
            HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json()['error'], 'User not found.')

    def test_update_a_user_profile(self):
        """
        Test update a user profile.
        """
        res = self.client.put(
            reverse('update_profile', kwargs={'username': 'test1'}),
            self.profile,
            HTTP_AUTHORIZATION=self.auth_header,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['message'],
                         'Profile successfully updated.')

    def test_update_a_user_profile_forbidden_request(self):
        """
        Test update a user profile forbidden request.
        """
        # login another user
        login_response = self.client.post(
            reverse('user_login'),
            self.login_data_two,
            format='json')
        token = login_response.json()['token']
        auth_header = 'Bearer {}'.format(token)
        # update profile
        res = self.client.put(
            reverse('update_profile', kwargs={'username': 'test1'}),
            self.profile,
            HTTP_AUTHORIZATION=auth_header,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            res.json()['error'], 'You do not have permissions to edit this profile.')
