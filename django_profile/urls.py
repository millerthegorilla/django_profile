from django import urls

from . import views as profile_views

app_name = "django_profile"
urlpatterns = [
    urls.path(
        "profile/", profile_views.ProfileUpdate.as_view(), name="profile_update_view"
    ),
]
