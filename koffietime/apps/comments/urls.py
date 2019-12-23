from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    CreateCommentsAPIView,
    RetrieveCommentsAPIView,
    UpdateCommentAPIView,
    DestroyCommentAPIView
)

urlpatterns = [
    path('posts/<slug:slug>/comments/create', CreateCommentsAPIView.as_view(),
         name='create_comments'),
    path('posts/<slug:slug>/comments', RetrieveCommentsAPIView.as_view(),
         name='retrieve_comments'),
    path('posts/<slug:slug>/comments/<int:id>/update',
         UpdateCommentAPIView.as_view(), name='update_comment'),
    path('posts/<slug:slug>/comments/<int:id>/delete',
         DestroyCommentAPIView.as_view(), name='delete_comment'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
