from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from koffietime.apps.posts.models import Post
from .models import Like


class LikeDislikePostView(APIView):
    """
    Handles GET requests for liking a post.
    If `True` then `dislike` a post, and if `False` then
    `like` the post.
    returns:
    - success message
    - likes count
    """

    permission_classes = [IsAuthenticated]

    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound({'error': 'Post not found.'})

    def get_like(self, post_id, user_id):
        try:
            return Like.objects.get(post=post_id, user=user_id)
        except Like.DoesNotExist:
            return None

    def get(self, request, post_id):
        post = self.get_post(post_id)
        like = self.get_like(post_id, request.user.id)
        likes = 0
        message = None
        # Dislike a post.
        if like:
            like.delete()
            if likes > 0:
                likes = post.likes - 1
            message = 'Post successfully disliked.'
        elif not post.user.id == request.user.id:
            # Like a post if it was not created by the current user.
            like = Like(post=post, user=request.user)
            like.save()
            likes = post.likes + 1
            message = 'Post successfully likes.'
        else:
            # Otherwise return a bad request error.
            return Response({'error': 'You can not like your own post!'},
                            status=status.HTTP_400_BAD_REQUEST)
        Post.objects.filter(id=post_id).update(likes=likes)
        return Response({'message': message, 'likes': likes},
                        status=status.HTTP_200_OK)
