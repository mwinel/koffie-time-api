from django.urls import path

from .views import UserSignupAPIView, UserLoginAPIView


urlpatterns = [
    path('auth/signup', UserSignupAPIView.as_view(), name='user_signup'),
    path('auth/login', UserLoginAPIView.as_view(), name='user_login')
]
