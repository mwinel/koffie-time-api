from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from .models import Post
from .serializers import PostsSerializer
from .pagination import PostsPagination, PaginationHandlerMixin


def get_object(slug):
    try:
        return Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise NotFound({'error': 'Post not found.'})


class CreatePostAPIView(APIView):
    """
    Handles POST requests for posts.
    returns:
    - post object
    - success message
    """

    serializer_class = PostsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response({
            'post': serializer.data,
            'message': 'Post successfully created.'
        }, status=status.HTTP_201_CREATED)


class RetrievePostsAPIView(APIView, PaginationHandlerMixin):
    """
    Handles GET requests for posts, including pagination.
    returns:
    - a list of paginated posts
    - total number of posts i.e: `count`
    - next url
    - prev url
    """

    pagination_class = PostsPagination
    serializer_class = PostsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = []

    def get(self, request, format=None, *args, **kwargs):
        posts = Post.objects.all()
        page = self.paginate_queryset(posts)
        if page:
            serializer = self.get_paginated_response(
                self.serializer_class(page, many=True).data)
        return Response({'posts': serializer.data}, status=status.HTTP_200_OK)


class RetrievePostAPIView(APIView):
    """
    Handles GET requests for a post.
    params:
    - post slug
    returns:
    - post object
    """

    serializer_class = PostsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = []

    def get(self, request, slug, format=None):
        post = get_object(slug)
        serializer = self.serializer_class(post)
        return Response({'post': serializer.data})


class UpdatePostAPIView(APIView):
    """
    Handles PUT requests for a post.
    params:
    - post slug
    returns:
    - post object
    - success message
    """

    serializer_class = PostsSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, slug, format=None):
        post = get_object(slug)
        if post.user == request.user:
            serializer = self.serializer_class(post, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'post': serializer.data,
                'message': 'Post successfully updated.'},
                status=status.HTTP_200_OK)
        return Response({
            'error': 'You do not have permissions to edit this post.'
        }, status=status.HTTP_403_FORBIDDEN)


class DestroyPostAPIView(APIView):
    """
    Handles DELETE requests for a post.
    params:
    - post slug
    returns:
    - success message
    """

    serializer_class = PostsSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, slug, format=None):
        post = get_object(slug)
        if post.user == request.user:
            post.delete()
            return Response({
                'message': 'Post successfully deleted.'},
                status=status.HTTP_204_NO_CONTENT)
        return Response({
            'error': 'You do not have permissions to delete this post.'
        }, status=status.HTTP_403_FORBIDDEN)
