from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    CharField,
    ReadOnlyField
)

from .models import Post
from koffietime.apps.authentication.serializers import UserSerializer


class PostsSerializer(ModelSerializer):
    """
    Maps complex `post` querysets and model instances to be
    converted to native Python datatypes that are easily rendered
    into other content types such as `JSON` and `XML`.
    """

    title = CharField(
        required=True,
        error_messages={
            'blank': 'Title field cannot be left blank.'
        }
    )

    body = CharField(
        required=True,
        error_messages={
            'blank': 'Body field cannot be left blank.'
        }
    )

    image = CharField(
        required=True,
        error_messages={
            'blank': 'Image field cannot be left blank.'
        }
    )

    category = CharField(
        required=True,
        error_messages={
            'blank': 'Category field cannot be left blank.'
        }
    )

    user = ReadOnlyField(source='user.username')

    def validate_title(self, title):
        post_exists = Post.objects.filter(title=title).exists()
        if post_exists:
            raise ValidationError(
                'Post with a similar title already exists, try something better.')
        return title

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'body',
            'image',
            'category',
            'tags',
            'slug',
            'likes',
            'draft',
            'public',
            'reported',
            'report_count',
            'read_time',
            'created_on',
            'updated_on',
            'user'
        )
        read_only_fields = ('created_on', 'updated_on', 'user')
