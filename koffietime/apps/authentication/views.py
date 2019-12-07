from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserSignupSerializer, UserLoginSerializer


class UserSignupAPIView(APIView):
    """
    Handles POST request to create a new user.
    returns:
    - user object
    - success message
    """

    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'user': serializer.data,
                'message': 'User successfully created.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    """
    Handles POST request to login a user.
    returns:
    - JWT auth token
    - success message
    """

    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = User.encode_auth_token(
            serializer.data['username']).decode('utf-8')
        response = {
            'token': token,
            'message': 'Successfully logged in.',
        }
        return Response(response, status=status.HTTP_200_OK)
