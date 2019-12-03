from datetime import datetime

from django.db import models
from django.db.models.signals import pre_save
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse

from .utils import unique_slug_generator


class Post(models.Model):
    """
        Model class for creating a post.
    """
    title = models.CharField(max_length=225)
    slug = models.SlugField(max_length=225, null=True)
    body = models.TextField()
    image = models.CharField(max_length=500, null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    category = models.TextField(null=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    public = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)
    report_count = models.IntegerField(default=0)
    read_time = models.TextField(default="less than a minute.")
    created_on = models.DateTimeField(
        auto_now_add=True, editable=False, null=True)
    updated_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        """
            Returns: string representaion of the post model class.
        """
        return self.title


def slug_generator(sender, instance, *args, **kwargs):
    """
        Generates a slug.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Post)
