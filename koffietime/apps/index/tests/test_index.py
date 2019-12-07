from django.urls import reverse

from rest_framework import status

from .base import BaseTestCase


class IndexTestCase(BaseTestCase):

    def test_index(self):
        """
        Test API returns a welcome message.
        """
        url = reverse('index_details')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Welcome to koffie time.')
