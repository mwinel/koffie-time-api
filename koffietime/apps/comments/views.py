from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny
)

from .models import Comment
from .serializers import CommentSerializer
from koffietime.core.utils import get_post_by_slug, get_comment_by_id


class CreateCommentsAPIView(APIView):
    """
    Handles Post requests for comments on a given post.
    returns:
    - comment object
    - success message
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, AllowAny]

    def post(self, request, slug):
        post = get_post_by_slug(slug)
        comment = request.data
        comment['post'] = post.id
        serializer = self.serializer_class(data=comment)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response({
            'comment': serializer.data,
            'message': 'Comment successfully created.'
        }, status=status.HTTP_201_CREATED)


class RetrieveCommentsAPIView(APIView):
    """
    Handles GET requests for comments on a given post.
    returns:
    - a list of comments
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = []

    def get(self, request, slug):
        post = get_post_by_slug(slug)
        queryset = Comment.objects.filter(post=post)
        serializer = self.serializer_class(queryset, many=True)
        return Response({'comments': serializer.data},
                        status=status.HTTP_200_OK)


class UpdateCommentAPIView(APIView):
    """
    Handles PUT requests for a omment on a given post.
    params:
    - post slug
    - comment id
    returns:
    - post object
    - success message
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, id, slug):
        post = get_post_by_slug(slug)
        comment = get_comment_by_id(id)
        if comment.user.username == request.user.username:
            data = {}
            data['post'] = post.id
            data['body'] = request.data['body']
            serializer = self.serializer_class(comment, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'comment': serializer.data,
                'message': 'Comment successfully updated.'},
                status=status.HTTP_200_OK)
        return Response({
            'error': 'You do not have permissions to edit this comment.'
        }, status=status.HTTP_403_FORBIDDEN)


class DestroyCommentAPIView(APIView):
    """
    Handles DELETE requests for a comment given a post.
    params:
    - post slug
    - comment id
    returns:
    - success message
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, id, slug):
        get_post_by_slug(slug)
        comment = get_comment_by_id(id)
        if comment.user.username == request.user.username:
            comment.delete()
            return Response({
                'message': 'Comment successfully deleted.'},
                status=status.HTTP_204_NO_CONTENT)
        return Response({
            'error': 'You do not have permissions to delete this post.'
        }, status=status.HTTP_403_FORBIDDEN)
