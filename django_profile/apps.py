import os
from collections import OrderedDict
import django
from django.apps import apps
from django.core import management
from django.conf import settings

from django_users import templates as user_templates
from captcha import templates as captcha_templates


class DjangoProfileConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_profile"

    def ready(self) -> None:
        new_app_name = "captcha"

        if new_app_name not in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS += (new_app_name,)
            apps.app_configs = OrderedDict()
            apps.apps_ready = apps.models_ready = apps.loading = apps.ready = False
            apps.clear_cache()
            apps.populate(settings.INSTALLED_APPS)

            # management.call_command("makemigrations", new_app_name, interactive=False)

            # management.call_command("migrate", new_app_name, interactive=False)

        settings.TEMPLATES[0]["DIRS"].append(
            os.path.abspath(user_templates.__path__._path[0])
        )
        settings.TEMPLATES[0]["DIRS"].append(
            os.path.abspath(captcha_templates.__path__._path[0])
        )
