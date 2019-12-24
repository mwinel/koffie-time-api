from rest_framework.exceptions import NotFound

from koffietime.apps.posts.models import Post
from koffietime.apps.comments.models import Comment


def get_post(slug):
    """
    Returns an post by its slug.
    """
    try:
        return Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise NotFound({'error': 'Post not found.'})


def get_comment(id):
    """
    Returns a comment by its id.
    """
    try:
        return Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        raise NotFound({'error': 'Comment not found.'})
