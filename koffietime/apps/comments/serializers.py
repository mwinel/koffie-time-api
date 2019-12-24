from rest_framework.serializers import (
    ModelSerializer,
    ReadOnlyField
)

from .models import Comment


class CommentSerializer(ModelSerializer):
    """
    Maps complex `Comment` querysets and model instances to be
    converted to native Python datatypes that are easily rendered
    into other content types such as `JSON` and `XML`.
    """

    user = ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = '__all__'
