import jwt
import datetime

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
    """
    To create a custom user, we need to define our own Manager class.
    By inheriting from `BaseUserManager` and overriding the `create_user`
    function, we are able to extend the 'User` class.
    """

    def create_user(self, username, email, password=None):
        """
        Create a user.
        returns:
        - a `User` with an email, username and password.
        """
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email address.')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Create a `User` with superuser powers.
        Superuser powers means that this use is an admin that can
        do anything they want.
        returns:
        - a `User` with an email, username and password.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.email_verified = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model class.
    """
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # The `email_verified` flag represents whether the registered user has a
    # verified account. The user verifys their account through a link sent
    # to their email.
    email_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # More fields required by Django when specifying a custom user model.

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case, we want it to be the email field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns string representaion of the user model class.
        """
        return self.username

    def get_short_name(self):
        """
        Returns users username.
        """
        return self.username

    @staticmethod
    def encode_auth_token(email):
        """
        Generates auth (JWT) token.
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': email
            }
            return jwt.encode(
                payload, settings.SECRET_KEY, algorithm='HS256'
            )
        except Exception as e:
            return e
