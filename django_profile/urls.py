from django.urls import include, path
from django_users import urls as django_users_urls
from . import urls_app as profile_urls

urlpatterns = [
    path(
        "",
        include(django_users_urls, namespace="django_users"),
        {"namespace": "django_users"},
    ),
    path("", include(profile_urls, namespace="django_profile")),
]
