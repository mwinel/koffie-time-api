from django.urls import path

from .views import Index

urlpatterns = [
    path('', Index.as_view(), name='index_details'),
    path('index', Index.as_view(), name='index_details')
]
