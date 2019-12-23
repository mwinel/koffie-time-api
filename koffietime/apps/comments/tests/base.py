from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient

from koffietime.apps.posts.models import Post
from koffietime.apps.comments.models import Comment


User = get_user_model()


class BaseTestCase(APITestCase):
    """
    Base Test Cases for comments crud.
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
        # Create user 2.
        self.user2 = User.objects.create_user(
            email='test2@gmail.com',
            username='test2',
            password='test@2'
        )
        self.user2.save()

        # login data user 1
        self.login_data = {
            'email': self.user.email,
            'password': 'test@1'
        }

        # login data user 2
        self.login_data_user_two = {
            'email': self.user2.email,
            'password': 'test@2'
        }

        self.login = reverse('user_login')
        # Login user 1
        self.login_response = self.client.post(
            self.login,
            self.login_data,
            format='json'
        )
        auth_token = self.login_response.json()['token']
        self.auth_header = 'Bearer {}'.format(auth_token)

        self.post = Post.objects.create(
            title='Post',
            body='Body',
            image='image1',
            category='engineering',
            tags=['python', 'aws'],
        )

        self.create_post_data = {
            'title': 'Post 1',
            'body': 'Body 1',
            'image': 'image1',
            'category': 'engineering',
            'tags': ['python', 'aws']
        }

        self.create_post = self.client.post(
            reverse('create_posts'),
            self.create_post_data,
            HTTP_AUTHORIZATION=self.auth_header,
            format='json'
        )

        self.comment = Comment.objects.create(
            body='This is a comment.',
            post=self.post,
            user=self.user
        )

        self.comment_data = {
            'body': 'This is a comment.'
        }

        self.update_comment_data = {
            'body': 'This is a comment update.'
        }
