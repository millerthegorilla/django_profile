import pytest


from django_profile import forms as profile_forms


def test_user_profile_with_data(db, active_user, user_details):
    form = profile_forms.UserProfile(user_details.__dict__)
    for field in form.fields:
        assert active_user.__dict__[field] == form[field].value()


def test_user_profile_validation_email(db, user_details):
    bob = user_details.__dict__
    bob["email"] = "bob@bo"
    form = profile_forms.UserProfile(bob)
    assert len(form.errors) == 1
    assert form.errors["email"][0] == "Enter a valid email address."


def test_user_profile_rejects_existing_user(db, active_user):
    form = profile_forms.UserProfile(active_user.__dict__)
    assert len(form.errors) == 1
    assert form.errors["username"][0] == "A user with that username already exists."


def test_profile_excludes_profile_user():
    form = profile_forms.Profile()
    with pytest.raises(KeyError):
        form["profile_user"]
