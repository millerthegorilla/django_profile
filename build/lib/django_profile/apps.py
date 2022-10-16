import os
from django import apps
from django.conf import settings

from django_users import templates as user_templates
from captcha import templates as captcha_templates


class DjangoProfileConfig(apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_profile"

    def ready(self) -> None:
        settings.TEMPLATES[0]["DIRS"].append(
            os.path.abspath(user_templates.__path__._path[0])
        )
        settings.TEMPLATES[0]["DIRS"].append(
            os.path.abspath(captcha_templates.__path__._path[0])
        )
