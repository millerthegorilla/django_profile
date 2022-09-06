import logging

from crispy_bootstrap5 import bootstrap5
from crispy_forms import helper, layout
from django import db, forms
from django.contrib.auth import get_user_model

from . import models as profile_models

# TODO: need to setup clamav.conf properly


logger = logging.getLogger("django_artisan")


class UserProfile(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        try:
            self.initial = kwargs["initial"]
        except KeyError:
            pass
        for fieldname in ["username", "email"]:
            self.fields[fieldname].help_text = None
        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.css_class = ""
        self.helper.layout = layout.Layout(
            bootstrap5.FloatingField("username"),
            bootstrap5.FloatingField("email"),
            bootstrap5.FloatingField("first_name"),
            bootstrap5.FloatingField("last_name"),
        )

    def clean_email(self) -> str:
        email = self.cleaned_data["email"]
        try:
            if email != self.initial["email"]:
                try:
                    if not get_user_model().objects.filter(email=email).exists():
                        return email
                    else:
                        self.valid = False
                        self.add_error("email", "Error! That email already exists!")
                except db.IntegrityError as e:
                    error_message = e.__cause__
                    logger.error(error_message)
            return email
        except KeyError:
            return email

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "first_name", "last_name"]
        exclude = ["profile_user"]


class Profile(forms.ModelForm):
    class Meta:
        model = profile_models.Profile
        fields = [
            "profile_user",
        ]
        exclude = ["profile_user"]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = helper.FormHelper()
        self.helper.css_class = ""
        self.helper.form_tag = False
