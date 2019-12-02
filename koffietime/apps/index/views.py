from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Index(APIView):

    def get(self, request, *args, **kwargs):
        """
           Returns: koffie time welcome message.
        """
        return Response({'message': 'Welcome to koffie time.'}, status=status.HTTP_200_OK)
