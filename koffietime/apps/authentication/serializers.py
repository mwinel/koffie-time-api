import re

from django.contrib.auth.hashers import check_password

from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
    ValidationError
)

from .models import User


class UserSignupSerializer(ModelSerializer):
    """
    Maps complex `User` querysets and model instances to be
    converted to native Python datatypes that are easily rendered
    into other content types such as `JSON` and `XML`.
    """

    email = EmailField()
    username = CharField(trim_whitespace=True)
    password = CharField(
        write_only=True,
        required=True,
        error_messages={
            'blank': 'Password field cannot be left empty.'
        }
    )

    def validate_email(self, email):
        """
        Validates email.
        """
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise ValidationError('Email provided already exists.')
        return email

    def validate_username(self, username):
        """
        Validates username.
        - check if provided username already exists
        - username should be longer than 4 characters
        - username should not contain white spaces
        """
        username_exists = User.objects.filter(username=username).exists()
        if username_exists:
            raise ValidationError(
                'Username provided already exists.')
        return username

    class Meta:
        model = User
        fields = ['email', 'username', 'password']


class UserLoginSerializer(ModelSerializer):
    email = CharField(max_length=255, required=True)
    username = CharField(max_length=255, read_only=True)
    password = CharField(
        max_length=128,
        write_only=True,
        required=True,
    )

    def get_user_object(self, email):
        try:
            return User.objects.get(email=email)
        # If no user was found matching the email combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        except User.DoesNotExist:
            raise ValidationError('User does not exist.')

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        user = self.get_user_object(email)

        # If no user was found matching the password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        password_valid = check_password(password, user.password)
        if not password_valid:
            raise ValidationError(
                'The email or password you entered is incorrect. Please try again.')

        # Check if user is still active and not banned. If user is banned
        # raise an exception in this case.
        if not user.is_active:
            raise ValidationError(
                'This user has been deactivated.')

        # Check if account is activated. If not, raise an exception in
        # this case.
        # if not user.email_verified:
        #     raise ValidationError(
        #         'Account not yet activated. Check email for activation link.')

        # The validated method returns a dictonary of validated data.
        return {
            'email': user.email,
            'username': user.username
        }

    class Meta:
        model = User
        fields = ['email', 'username', 'password']


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
