from django.urls import reverse

from rest_framework import status

from .base import BaseTestCase


class PostsCrudTestCase(BaseTestCase):
    """
    Test cases for post crud functionality.
    """

    def test_post_model_returns_string_object(self):
        """
        Test post object string representation is returned.
        """
        self.assertTrue(self.post.body, str(self.post))

    def test_create_post(self):
        """
        Test create post.
        """
        res = self.create_post
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            res.json()['message'], 'Post successfully created.')

    def test_create_post_with_similar_title(self):
        """
        Test create post with similar title.
        """
        self.create_post
        res = self.client.post(
            reverse('create_posts'),
            self.create_post_data,
            HTTP_AUTHORIZATION=self.auth_header,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['title'], [
                         'Post with a similar title already exists, try something better.'])

    def test_get_posts(self):
        """
        Test get all posts.
        """
        res = self.client.get(
            reverse('retrieve_posts'),
            HTTP_AUTHORIZATION=self.auth_header,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_post(self):
        """
        Test get a single post.
        """
        res = self.client.get(
            reverse('retrieve_post', kwargs={'slug': 'post'}),
            HTTP_AUTHORIZATION=self.auth_header,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_post_that_does_not_exist(self):
        """
        Test get a single post that does not exist.
        """
        res = self.client.get(
            reverse('retrieve_post', kwargs={'slug': 'post-does-not-exist'}),
            HTTP_AUTHORIZATION=self.auth_header,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_a_post(self):
        """
        Test update a post.
        """
        # create a post
        self.create_post
        # update post
        res = self.client.put(
            reverse('update_post', kwargs={'slug': 'post-1'}),
            self.update_post_data,
            HTTP_AUTHORIZATION=self.auth_header,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['message'], 'Post successfully updated.')

    def test_update_a_post_forbidden_request(self):
        """
        Test update a post forbidden request.
        """
        # create a post
        self.create_post
        # login another user
        login_response = self.client.post(
            reverse('user_login'),
            self.login_data_two,
            format='json')
        token = login_response.json()['token']
        auth_header = 'Bearer {}'.format(token)
        # update post
        res = self.client.put(
            reverse('update_post', kwargs={'slug': 'post-1'}),
            self.update_post_data,
            HTTP_AUTHORIZATION=auth_header,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            res.json()['error'], 'You do not have permissions to edit this post.')

    def test_delete_a_post(self):
        """
        Test delete a post.
        """
        # create a post
        self.create_post
        # delete post
        res = self.client.delete(
            reverse('delete_post', kwargs={'slug': 'post-1'}),
            HTTP_AUTHORIZATION=self.auth_header,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_a_post_forbidden_request(self):
        """
        Test delete a post forbidden request.
        """
        # create a post
        self.create_post
        # login another user
        login_response = self.client.post(
            reverse('user_login'),
            self.login_data_two,
            format='json')
        token = login_response.json()['token']
        auth_header = 'Bearer {}'.format(token)
        # delete post
        res = self.client.delete(
            reverse('delete_post', kwargs={'slug': 'post-1'}),
            HTTP_AUTHORIZATION=auth_header,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            res.json()['error'], 'You do not have permissions to delete this post.')
