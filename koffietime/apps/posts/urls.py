from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    CreatePostAPIView,
    RetrievePostsAPIView,
    RetrievePostAPIView,
    UpdatePostAPIView,
    DestroyPostAPIView
)

urlpatterns = [
    path('posts/', RetrievePostsAPIView.as_view(), name='retrieve_posts'),
    path('posts/create', CreatePostAPIView.as_view(), name='create_posts'),
    path('posts/<slug:slug>', RetrievePostAPIView.as_view(),
         name='retrieve_post'),
    path('posts/<slug:slug>/update', UpdatePostAPIView.as_view(),
         name='update_post'),
    path('posts/<slug:slug>/delete', DestroyPostAPIView.as_view(),
         name='delete_post'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
