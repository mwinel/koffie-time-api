from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    RetrieveUserProfilesAPIView,
    RetrieveUserProfileAPIView,
    UpdateUserProfileAPIView
)

urlpatterns = [
    path('profiles/', RetrieveUserProfilesAPIView.as_view(),
         name='retrieve_profiles'),
    path('profiles/<str:username>/',
         RetrieveUserProfileAPIView.as_view(), name='retrieve_profile'),
    path('profiles/<str:username>/update',
         UpdateUserProfileAPIView.as_view(), name='update_profile')
]

urlpatterns = format_suffix_patterns(urlpatterns)
