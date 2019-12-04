from rest_framework.serializers import ValidationError

from .models import Post


class PostValidations:
    """
        Validates post on creation.
    """

    def validate_title(self, title):
        """
            Checks if post exists given its title.
        """
        post_exists = Post.objects.filter(title=title).exists()
        if post_exists:
            raise ValidationError(
                'Post with a similar title already exists, try something better.')
