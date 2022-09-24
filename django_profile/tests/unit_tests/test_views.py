from django.contrib.auth import get_user_model

from django_profile import forms as profile_forms
from bs4 import BeautifulSoup


User = get_user_model()


def test_get_correct_status_code(profile_get_response):
    assert profile_get_response.status_code == 200


def test_get_correct_content(profile_get_response, user):
    soup = BeautifulSoup(profile_get_response.content, features="html.parser")
    assert user.username == soup.find(id="id_username").get("value")
    assert user.email == soup.find(id="id_email").get("value")
    assert user.first_name == soup.find(id="id_first_name").get("value")
    assert user.last_name == soup.find(id="id_last_name").get("value")


def test_get_context_returns_forms(profile_update):
    context = profile_update.get_context_data()
    assert type(context["form"]) == profile_forms.Profile
    assert type(context["user_form"]) == profile_forms.UserProfile


def test_posts_correct_response_and_changes_data(profile_update, profile_post_request):
    response = profile_update.post(profile_post_request(first_name="bob"))
    assert response.status_code == 302
    assert User.objects.first().first_name == "bob"


def test_posts_with_incorrect_data_returns_correct_response(
    profile_update, profile_post_request
):
    response = profile_update.post(profile_post_request(email="bob@bob"))
    soup = BeautifulSoup(response.content, features="html.parser")
    assert soup.find(id="error_1_id_email").get_text() == "Enter a valid email address."
