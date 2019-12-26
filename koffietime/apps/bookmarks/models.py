from django.db import models

from koffietime.apps.authentication.models import User
from koffietime.apps.posts.models import Post


class Bookmark(models.Model):
    """
    Model class for creating a bookmark.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
