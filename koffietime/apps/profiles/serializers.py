from rest_framework.serializers import (
    ModelSerializer,
    CharField
)

from .models import UserProfile


class UserProfileSerializer(ModelSerializer):
    """
    Maps complex `User Profile` querysets and model instances to be
    converted to native Python datatypes that are easily rendered
    into other content types such as `JSON` and `XML`.
    """

    username = CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('updated_on', 'user')
