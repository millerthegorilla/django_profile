import os
from collections import OrderedDict
import django
from django.apps import apps
from django.conf import settings

from django_users import templates as user_templates


APPS = [
    {"name": "django_users", "templates": user_templates},
]


class DjangoProfileConfig(django.apps.AppConfig):
    """idea taken from
    https://stackoverflow.com/questions/24027901/dynamically-loading-django-apps-at-runtime/57897422#57897422"""  # noqa: E501

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_profile"

    def ready(self) -> None:
        for app in APPS:
            breakpoint()
            if app["name"] not in settings.INSTALLED_APPS:
                settings.INSTALLED_APPS += (app["name"],)
                apps.app_configs = OrderedDict()
                apps.apps_ready = apps.models_ready = apps.loading = apps.ready = False
                apps.clear_cache()
                apps.populate(settings.INSTALLED_APPS)
                if app["templates"] != "":
                    settings.TEMPLATES[0]["DIRS"].append(
                        os.path.abspath(app["templates"].__path__._path[0])
                    )
