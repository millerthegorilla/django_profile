import os
import importlib
from collections import OrderedDict

from django.apps import apps, AppConfig
from django.conf import settings
from django.core.management import call_command

from django_users import templates as user_templates


my_apps = [
    {"name": "django_users", "templates": user_templates},
]


class DjangoProfileConfig(AppConfig):
    """idea taken from
    https://stackoverflow.com/questions/24027901/dynamically-loading-django-apps-at-runtime/57897422#57897422"""  # noqa: E501

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_profile"

    def ready(self) -> None:
        global my_apps
        try:
            if not settings.TOPLEVELCONFIG:
                settings.TOPLEVELCONFIG = self.__class__
                self.populate_my_apps()
                self.install_apps()
        except AttributeError:
            settings.TOPLEVELCONFIG = self.__class__
            self.populate_my_apps()
            self.install_apps()

    def populate_my_apps(self):
        global my_apps
        for app in my_apps:
            try:
                theapp = importlib.import_module(app["name"] + ".apps")
                my_apps += [app for app in theapp.my_apps if app not in my_apps]
                app["setup"] = theapp.setup_apps
            except (ModuleNotFoundError, AttributeError):
                pass

    def install_apps(self):
        for app in my_apps:
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
                if "setup" in app:
                    app["setup"]()
        # static = os.path.abspath(
        #     importlib.import_module(app["name"]).__path__[0] + "/static/"
        # )
        # if os.path.isdir(static):
        #     sdir = True
        #     settings.STATICFILES_DIRS += [static]

        # if sdir:
        #     call_command("collectstatic", verbosity=0, interactive=False)

    # setup_apps()
