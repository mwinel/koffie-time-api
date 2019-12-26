from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import CreateDestroyBookmarkView, RetrieveBookmarksView

urlpatterns = [
    path('posts/<int:post_id>/bookmark', CreateDestroyBookmarkView.as_view(),
         name='bookmark_post'),
    path('posts/<slug:slug>/bookmarks', RetrieveBookmarksView.as_view(),
         name='retrieve_bookmarks')
]

urlpatterns = format_suffix_patterns(urlpatterns)
