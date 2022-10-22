import os
import importlib
from collections import OrderedDict

from django.apps import apps, AppConfig
from django.conf import settings

from django_users import templates as user_templates


my_apps = [
    {"name": "django_users.apps.DjangoUsersConfig", "templates": user_templates},
]


class DjangoProfileConfig(AppConfig):
    """idea taken from
    https://stackoverflow.com/questions/24027901/dynamically-loading-django-apps-at-runtime/57897422#57897422"""  # noqa: E501

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_profile"

    def ready(self) -> None:
        global my_apps
        for app in my_apps:
            if app["name"] not in settings.INSTALLED_APPS:
                theapp = importlib.import_module(app["name"] + ".apps")
                try:
                    my_apps += theapp.my_apps
                except AttributeError:
                    pass
                settings.INSTALLED_APPS += (app["name"],)
                apps.app_configs = OrderedDict()
                apps.apps_ready = apps.models_ready = apps.loading = apps.ready = False
                apps.clear_cache()
                apps.populate(settings.INSTALLED_APPS)
                if app["templates"] != "":
                    settings.TEMPLATES[0]["DIRS"].append(
                        os.path.abspath(app["templates"].__path__._path[0])
                    )
