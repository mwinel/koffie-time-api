from rest_framework import serializers

from .models import Post
from .validations import PostValidations

validators = PostValidations()


class PostSerializer(serializers.ModelSerializer):
    """
        This class maps the `Post` model instance
        into JSON format.
    """

    title = serializers.CharField(
        required=True,
        error_messages={
            'blank': 'Title field cannot be left blank.'
        },
        validators=[validators.validate_title]
    )
    body = serializers.CharField(
        required=True,
        error_messages={
            'blank': 'Body field cannot be left blank.'
        }
    )
    image = serializers.CharField(
        required=True,
        error_messages={
            'blank': 'Image field cannot be left blank.'
        }
    )
    category = serializers.CharField(
        required=True,
        error_messages={
            'blank': 'Category field cannot be left blank.'
        }
    )

    class Meta:
        model = Post
        # Return all of the comment fields that could possibly be included in a
        # request or response, including fields specified explicitly above
        fields = '__all__'
        read_only_fields = ('created_on', 'updated_on')
