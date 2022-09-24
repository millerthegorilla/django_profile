import pytest

from django.contrib.auth import get_user_model
from django.db import IntegrityError

from django_profile import models as profile_models

User = get_user_model()


def test_create_a_user_creates_a_profile(user, db):
    profile = profile_models.Profile.objects.last()
    assert user.profile == profile


def test_create_a_profile_with_no_user_raises_integrity_error(db):
    with pytest.raises(IntegrityError):
        profile_models.Profile.objects.create()
