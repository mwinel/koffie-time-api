from django.db import models

from koffietime.apps.authentication.models import User
from koffietime.apps.posts.models import Post


class Like(models.Model):
    """
    Model class for creating post likes.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
