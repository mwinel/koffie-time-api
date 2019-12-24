from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny
)

from .models import UserProfile
from .serializers import UserProfileSerializer


def get_user(username):
    try:
        return UserProfile.objects.get(user__username=username) 
    except UserProfile.DoesNotExist:
        raise NotFound({'error': 'User not found.'})


class RetrieveUserProfilesAPIView(APIView):
    """
    Handles GET requests for user profiles.
    returns:
    - a list of user profiles
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = []

    def get(self, request, format=None, *args, **kwargs):
        profiles = UserProfile.objects.all()
        serializer = self.serializer_class(profiles, many=True)
        return Response({
            'profiles': serializer.data}, status=status.HTTP_200_OK)


class RetrieveUserProfileAPIView(APIView):
    """
    Handles GET requests for a user profile.
    params:
    - profile username
    returns:
    - post object
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = []

    def get(self, request, username, format=None):
        profile = get_user(username)
        serializer = self.serializer_class(profile)
        return Response({'profile': serializer.data})


class UpdateUserProfileAPIView(APIView):
    """
    Handles PUT requests for a user profile.
    params:
    - profile username
    returns:
    - profile object
    - success message
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    # def get_object(self):
    #     return get_object_or_404(
    #         self.get_queryset(), user__username=self.kwargs.get('username')
    #     )

    def put(self, request, username, format=None):
        profile = get_user(username)
        if profile.user == request.user:
            serializer = self.serializer_class(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'profile': serializer.data,
                'message': 'Profile successfully updated.'},
                status=status.HTTP_200_OK)
        return Response({
            'error': 'You do not have permissions to edit this profile.'
        }, status=status.HTTP_403_FORBIDDEN)
