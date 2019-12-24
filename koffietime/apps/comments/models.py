from django.db import models

from koffietime.apps.authentication.models import User
from koffietime.apps.posts.models import Post


class Comment(models.Model):
    """
    Model class for creating a post comment.
    """

    body = models.TextField()
    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments',
                             on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the `Comment` model instance.
        """
        return self.body
