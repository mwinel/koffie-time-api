from django.urls import reverse

from rest_framework import status

from .base import BaseTestCase


class BookmarksTestCase(BaseTestCase):
    """
    Test case for bookmarks functionality.
    """

    def test_bookmark_a_post(self):
        """
        Test bookmark a post.
        """
        post = self.create_post
        post_id = post.json()['post']['id']
        self.client.get(
            reverse('bookmark_post', kwargs={'post_id': post_id}),
            HTTP_AUTHORIZATION=self.auth_header_two,
            format='json')
        res = self.client.get(
            reverse('bookmark_post', kwargs={'post_id': post_id}),
            HTTP_AUTHORIZATION=self.auth_header_two,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['message'],
                         'Post successfully removed from bookmarks.')

    def test_user_cannot_bookmark_their_own_post(self):
        """
        Test user cannot bookmark their own post.
        """
        post = self.create_post
        post_id = post.json()['post']['id']
        res = self.client.get(
            reverse('bookmark_post', kwargs={'post_id': post_id}),
            HTTP_AUTHORIZATION=self.auth_header,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['error'],
                         'You can not bookmark your own post!')

    def test_bookmarking_a_non_existing_post(self):
        """
        Test bookmarking a non existing post.
        """
        res = self.client.get(
            reverse('bookmark_post', kwargs={'post_id': 100000}),
            HTTP_AUTHORIZATION=self.auth_header_two,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json()['error'], 'Post not found.')

    def test_get_bookmarks(self):
        """
        Test get bookmarks.
        """
        post = self.create_post
        slug = post.json()['post']['slug']
        res = self.client.get(
            reverse('retrieve_bookmarks', kwargs={'slug': slug}),
            HTTP_AUTHORIZATION=self.auth_header_two)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
