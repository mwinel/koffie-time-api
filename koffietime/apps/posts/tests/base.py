from rest_framework.test import APITestCase, APIClient

from koffietime.apps.posts.models import Post


class BaseTestCase(APITestCase):
    """
       Base Test Cases for posts.
    """

    def setUp(self):
        # Initialize test client.
        self.client = APIClient()

        self.post = Post.objects.create(
            title='Post',
            body='Body',
            image='image1',
            category='engineering',
            tags=['python', 'aws']
        )

        self.create_post_data = {
            'title': 'Post 1',
            'body': 'Body 1',
            'image': 'image1',
            'category': 'engineering',
            'tags': ['python', 'aws']
        }

        self.create_post_data_missing_title = {
            'title': '',
            'body': 'Body 2',
            'image': 'image2',
            'category': 'engineering',
            'tags': ['python', 'aws']
        }

        self.update_post_data = {
            'title': 'Post one',
            'body': 'Body one',
            'image': 'image1',
            'category': 'engineering',
            'tags': ['python', 'aws']
        }
