from rest_framework.exceptions import NotFound

from koffietime.apps.profiles.models import UserProfile
from koffietime.apps.posts.models import Post
from koffietime.apps.comments.models import Comment


def get_user_by_username(username):
    """
    Returns a user object given the `username`.
    """
    try:
        return UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist:
        raise NotFound({'error': 'User not found.'})


def get_post_by_slug(slug):
    """
    Returns a post object given the `slug`.
    """
    try:
        return Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise NotFound({'error': 'Post not found.'})


def get_post_by_id(id):
    """
    Returns a post object given the `id`.
    """
    try:
        return Post.objects.get(id=id)
    except Post.DoesNotExist:
        raise NotFound({'error': 'Post not found.'})


def get_comment_by_id(id):
    """
    Returns a comment object given the `id`.
    """
    try:
        return Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        raise NotFound({'error': 'Comment not found.'})
