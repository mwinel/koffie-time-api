from django.urls import reverse

from rest_framework import status

from .base import BaseTestCase


class LikesTestCase(BaseTestCase):
    """
    Test case for post likes functionality.
    """

    def test_like_dislike_a_post(self):
        """
        Test like or dislike a post.
        """
        post = self.create_post
        post_id = post.json()['post']['id']
        self.client.get(
            reverse('like_dislike_post', kwargs={'post_id': post_id}),
            HTTP_AUTHORIZATION=self.auth_header_two,
            format='json')
        res = self.client.get(
            reverse('like_dislike_post', kwargs={'post_id': post_id}),
            HTTP_AUTHORIZATION=self.auth_header_two,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['message'], 'Post successfully disliked.')

    def test_user_cannot_like_their_own_post(self):
        """
        Test user cannot like their own post.
        """
        post = self.create_post
        post_id = post.json()['post']['id']
        res = self.client.get(
            reverse('like_dislike_post', kwargs={'post_id': post_id}),
            HTTP_AUTHORIZATION=self.auth_header,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['error'],
                         'You can not like your own post!')

    def test_like_dislike_a_non_existing_post(self):
        """
        Test like or dislike a non existing post.
        """
        res = self.client.get(
            reverse('like_dislike_post', kwargs={'post_id': 100000}),
            HTTP_AUTHORIZATION=self.auth_header_two,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json()['error'], 'Post not found.')
