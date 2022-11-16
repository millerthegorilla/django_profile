from django import conf, dispatch
from django.contrib.auth import models as auth_models
from django.db import models


class Profile(models.Model):
    """
    user profile
    """

    profile_user: models.OneToOneField = models.OneToOneField(
        auth_models.User, on_delete=models.CASCADE, related_name="profile"
    )

    def __str__(self) -> str:
        return str(self._meta.get_fields(include_hidden=True))

    class Meta:
        try:
            abstract = conf.settings.ABSTRACTPROFILE
        except AttributeError:
            abstract = False
        app_label = "django_profile"


"""
    Custom signals to create and update user profile
"""


@dispatch.receiver(models.signals.post_save, sender=auth_models.User)
    if created:
        Profile.objects.create(profile_user=instance)
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        pass
