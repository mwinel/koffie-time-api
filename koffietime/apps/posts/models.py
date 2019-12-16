from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify

from koffietime.apps.authentication.models import User


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
    draft = models.BooleanField(default=True)
    public = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)
    report_count = models.IntegerField(default=0)
    read_time = models.TextField(default="less than a minute.")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='posts',
                             on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        """
        Returns a string representaion of the post model class.
        """
        return self.title

    def save(self, *args, **kwargs):
        """
        Returns title slug.
        """
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
