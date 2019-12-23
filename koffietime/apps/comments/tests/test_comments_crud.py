from django.urls import reverse

from rest_framework import status

from .base import BaseTestCase


class CommetTestCase(BaseTestCase):
    """
    Testcases for comments CRUD.
    """

    def test_comment_model_returns_string_object(self):
        """
        Test comment string representation is returned.
        """
        self.assertTrue(self.comment.body, str(self.comment))

    def test_post_comments(self):
        """
        Test post a comment on an a given post.
        """
        url = reverse('create_comments', kwargs={'slug': 'post'})
        res = self.client.post(
            url, self.comment_data,
            HTTP_AUTHORIZATION=self.auth_header,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.json()['message'],
                         'Comment successfully created.')

    def test_get_comments(self):
        """
        Test retrieve comments.
        """
        url = reverse('retrieve_comments', kwargs={'slug': 'post'})
        res = self.client.get(
            url, HTTP_AUTHORIZATION=self.auth_header, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_comments_article_not_found(self):
        """
        Test retrieve comments on article not found.
        """
        url = reverse('retrieve_comments', kwargs={'slug': 'new-post'})
        res = self.client.get(
            url, HTTP_AUTHORIZATION=self.auth_header, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json()['error'], 'Post not found.')

    def test_update_a_comment(self):
        """
        Test update a single comment.
        """
        # post a comment
        post_url = reverse('create_comments', kwargs={'slug': 'post'})
        res = self.client.post(
            post_url,
            self.comment_data,
            HTTP_AUTHORIZATION=self.auth_header,
            format="json")
        comment_id = res.json()['comment']['id']
        # update a comment
        url = reverse('update_comment',
                      kwargs={'slug': 'post-1', 'id': comment_id})
        res = self.client.put(
            url,
            self.update_comment_data,
            HTTP_AUTHORIZATION=self.auth_header,
            format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['message'],
                         'Comment successfully updated.')

    def test_update_a_comment_forbidden(self):
        """
        Test update a single comment for unauthorized user.
        """
        # post a comment
        post_url = reverse('create_comments', kwargs={'slug': 'post'})
        res = self.client.post(
            post_url,
            self.comment_data,
            HTTP_AUTHORIZATION=self.auth_header,
            format="json")
        comment_id = res.json()['comment']['id']
        # login another user
        login_response = self.client.post(
            reverse('user_login'),
            self.login_data_user_two,
            format='json')
        token = login_response.json()['token']
        auth_header = 'Bearer {}'.format(token)
        # update a comment
        url = reverse('update_comment',
                      kwargs={'slug': 'post-1', 'id': comment_id})
        res = self.client.put(
            url,
            self.update_comment_data,
            HTTP_AUTHORIZATION=auth_header,
            format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.json()['error'],
                         'You do not have permissions to edit this comment.')

    def test_delete_a_comment(self):
        """
        Test delete a single comment.
        """
        # post a comment
        post_url = reverse('create_comments', kwargs={'slug': 'post'})
        res = self.client.post(
            post_url,
            self.comment_data,
            HTTP_AUTHORIZATION=self.auth_header,
            format="json")
        comment_id = res.json()['comment']['id']
        # delete a comment
        url = reverse('delete_comment',
                      kwargs={'slug': 'post-1', 'id': comment_id})
        res = self.client.delete(
            url,
            self.update_comment_data,
            HTTP_AUTHORIZATION=self.auth_header,
            format="json")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_a_comment_forbidden(self):
        """
        Test delete a single comment for an unauthorized user.
        """
        # post a comment
        post_url = reverse('create_comments', kwargs={'slug': 'post'})
        res = self.client.post(
            post_url,
            self.comment_data,
            HTTP_AUTHORIZATION=self.auth_header,
            format="json")
        comment_id = res.json()['comment']['id']
        # login another user
        login_response = self.client.post(
            reverse('user_login'),
            self.login_data_user_two,
            format='json')
        token = login_response.json()['token']
        auth_header = 'Bearer {}'.format(token)
        # delete a comment
        url = reverse('delete_comment',
                      kwargs={'slug': 'post-1', 'id': comment_id})
        res = self.client.delete(
            url,
            self.update_comment_data,
            HTTP_AUTHORIZATION=auth_header,
            format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
