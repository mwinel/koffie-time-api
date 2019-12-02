from rest_framework.test import APITestCase, APIClient


class BaseTestCase(APITestCase):
    """
       Base Test Cases for index.
    """

    def setUp(self):
        # Initialize test client.
        self.client = APIClient()
