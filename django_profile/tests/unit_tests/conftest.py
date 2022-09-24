import pytest
from django_profile import views as profile_views


@pytest.fixture()
def profile_get_request(rf, user):
    request = rf.get("/profile")
    request.user = user
    return request


@pytest.fixture()
def profile_post_request(rf, user):
    def post_request(first_name=None, email=None):
        data = {
            "username": user.username,
            "email": user.email if email is None else email,
            "first_name": user.first_name if first_name is None else first_name,
            "last_name": user.last_name,
        }
        request = rf.post("/profile", data)
        request.user = user
        return request

    return post_request


@pytest.fixture()
def profile_update(profile_get_request):
    profile_update = profile_views.ProfileUpdate()
    profile_update.request = profile_get_request
    return profile_update


@pytest.fixture()
def profile_get_response(profile_update, profile_get_request):
    return profile_update.get(profile_get_request)
