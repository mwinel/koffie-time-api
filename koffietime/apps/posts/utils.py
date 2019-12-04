from django.utils.text import slugify


def unique_slug_generator(instance, new_slug=None, **kwargs):
    """
        Generates a slug from the post title.
    """
    slug = slugify(instance.title)
    return slug
