from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from koffietime.apps.authentication.models import User


class UserProfile(models.Model):
    """
    Model class for creating a user profile.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    image = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    firstname = models.CharField(blank=True, max_length=25)
    lastname = models.CharField(blank=True, max_length=25)
    location = models.CharField(max_length=30, blank=True)
    github_url = models.URLField(blank=True)
    linked_url = models.URLField(blank=True)
    portifolio_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Automatically create the user profile for new users that
    register on the platform.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Save user profile after they register.
    """
    instance.userprofile.save()
