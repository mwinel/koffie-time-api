from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status


class Index(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        """
        Returns: koffie time welcome message.
        """
        return Response({'message': 'Welcome to koffie time.'},
                        status=status.HTTP_200_OK)
