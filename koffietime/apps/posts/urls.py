from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ListCreatePosts, PostDetail

urlpatterns = [
    path('posts/', ListCreatePosts.as_view(), name='posts_list'),
    path('posts/<slug:slug>', PostDetail.as_view(), name='posts_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
