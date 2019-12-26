from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import LikeDislikePostView

urlpatterns = [
    path('posts/<int:post_id>/like', LikeDislikePostView.as_view(),
         name='like_dislike_post')
]

urlpatterns = format_suffix_patterns(urlpatterns)
