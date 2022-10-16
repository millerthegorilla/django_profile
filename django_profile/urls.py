from django.urls import include, path

from django_users import urls as django_users_urls

from . import views as profile_views

app_name = "django_profile"
urlpatterns = [
    path("profile/", profile_views.ProfileUpdate.as_view(), name="profile_update_view"),
]
