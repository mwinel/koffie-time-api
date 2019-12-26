from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from koffietime.apps.posts.models import Post
from koffietime.apps.posts.serializers import PostsSerializer
from .models import Bookmark


class CreateDestroyBookmarkView(APIView):
    """
    Handles GET requests for bookmarking posts.
    If `True`, the request will unbookmark the post,
    and if `False` the same request will bookmark the post.
    returns:
    - success message
    """

    permission_classes = [IsAuthenticated]

    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound({'error': 'Post not found.'})

    def get_bookmark(self, post_id, user_id):
        try:
            return Bookmark.objects.get(post=post_id, user=user_id)
        except Bookmark.DoesNotExist:
            return None

    def get(self, request, post_id):
        post = self.get_post(post_id)
        bookmark = self.get_bookmark(post_id, request.user.id)
        message = None
        # Unbookmark a post.
        if bookmark:
            bookmark.delete()
            message = 'Post successfully removed from bookmarks.'
        elif not post.user.id == request.user.id:
            # Bookmark a post if it was not created by the current user.
            bookmark = Bookmark(post=post, user=request.user)
            bookmark.save()
            message = 'Post successfully added to bookmarks.'
        else:
            return Response({'error': 'You can not bookmark your own post!'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': message}, status=status.HTTP_200_OK)


class RetrieveBookmarksView(APIView):
    """
    Handles GET requests for bookmarked posts.
    returns:
    - a list of bookmarked posts
    """

    permission_classes = [IsAuthenticated]
    serializer_class = PostsSerializer

    def get(self, request, slug):
        bookmarks = Bookmark.objects.filter(user=request.user)
        bookmarked_articles = []
        for bookmark in bookmarks:
            post = Post.objects.get(slug=bookmark.post.slug)
            serializer = self.serializer_class(
                post, many=False, context={'request': request})
            bookmarked_articles.append(serializer.data)
        return Response({'bookmarks': bookmarked_articles},
                        status=status.HTTP_200_OK)
