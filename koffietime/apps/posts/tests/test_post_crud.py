from django.urls import reverse

from rest_framework import status

from koffietime.apps.posts.models import Post
from .base import BaseTestCase


class PostCrudTestCase(BaseTestCase):
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
        url = reverse('posts_list')
        response = self.client.post(url, self.create_post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_bad_request(self):
        """
            Test create post successfully returns 400 bad error.
        """
        url = reverse('posts_list')
        response = self.client.post(
            url, self.create_post_data_missing_title, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_post_with_similar_title(self):
        """
            Test create post with similar title.
        """
        url = reverse('posts_list')
        response = self.client.post(
            url, self.create_post_data, format='json')
        res = self.client.post(
            url, self.create_post_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['title'], [
                         'Post with a similar title already exists, try something better.'])

    def test_get_posts(self):
        """
            Test get all posts.
        """
        url = reverse('posts_list')
        response = self.client.get(url, format='json', page_size=None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res = response.json()
        res['count'] = 0
        self.assertIn('Post', res['results'][0]['title'])

    def test_get_post(self):
        """
            Test get a single post.
        """
        url = reverse('posts_detail', kwargs={'slug': 'post'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_post_that_does_not_exist(self):
        """
            Test get a single post that does not exist.
        """
        url = reverse('posts_detail', kwargs={'slug': 'post-1'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_a_post(self):
        """
            Test update a post.
        """
        # create a post
        url = reverse('posts_list')
        response = self.client.post(
            url, self.create_post_data, format='json')
        # update post
        update_url = reverse('posts_detail', kwargs={'slug': 'post-1'})
        res = self.client.put(update_url, self.update_post_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_a_post_bad_request(self):
        """
            Test update a post on a bad request.
        """
        # create a post
        url = reverse('posts_list')
        response = self.client.post(
            url, self.create_post_data, format='json')
        # update post with exisiting post title
        update_url = reverse('posts_detail', kwargs={'slug': 'post-1'})
        res = self.client.put(update_url, self.create_post_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_a_post(self):
        """
            Test delete a post.
        """
        # create a post
        url = reverse('posts_list')
        response = self.client.post(
            url, self.create_post_data, format='json')
        # delete post with exisiting post title
        delete_url = reverse('posts_detail', kwargs={'slug': 'post-1'})
        res = self.client.delete(delete_url, format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
