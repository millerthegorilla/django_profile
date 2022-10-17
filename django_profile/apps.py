import os
from collections import OrderedDict
import django
from django.apps import apps
from django.core import management
from django.conf import settings

from django_users import templates as user_templates
from captcha import templates as captcha_templates


class DjangoProfileConfig(django.apps.AppConfig):
    """idea taken from
    https://stackoverflow.com/questions/24027901/dynamically-loading-django-apps-at-runtime/57897422#57897422"""  # noqa: E501

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_profile"

    def ready(self) -> None:
        new_app_name = "django_users"
        new_app_name2 = "captcha"
        if new_app_name not in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS += (new_app_name,)
            apps.app_configs = OrderedDict()
            apps.apps_ready = apps.models_ready = apps.loading = apps.ready = False
            apps.clear_cache()
            apps.populate(settings.INSTALLED_APPS)
            # management.call_command("makemigrations", new_app_name, interactive=False)
            # management.call_command("migrate", new_app_name, interactive=False)
            settings.TEMPLATES[0]["DIRS"].append(
                os.path.abspath(captcha_templates.__path__._path[0])
            )

        if new_app_name2 not in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS += (new_app_name2,)
            apps.app_configs = OrderedDict()
            apps.apps_ready = apps.models_ready = apps.loading = apps.ready = False
            apps.clear_cache()
            apps.populate(settings.INSTALLED_APPS)
            settings.TEMPLATES[0]["DIRS"].append(
                os.path.abspath(user_templates.__path__._path[0])
            )
