import logging

from crispy_forms import helper, layout
from crispy_bootstrap5 import bootstrap5

from django import forms, db
from django.contrib.auth import get_user_model

from . import models as profile_models
# TODO: need to setup clamav.conf properly


logger = logging.getLogger('django_artisan')

class UserProfile(forms.ModelForm):
    # def clean_username(self, *args, **kwargs):
    #     username = self.cleaned_data['username']
    #     if User.objects.filter(username=username):
    #         self.add_error('username', 'Error, That username already exists!')
    #     return username

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        try:
            self.initial = kwargs['initial']
            if self.initial:
                breakpoint()   # TODO
        except KeyError:
            pass
        for fieldname in ['username', 'email']:
            self.fields[fieldname].help_text = None
        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.css_class = ''
        self.helper.layout = layout.Layout(
            bootstrap5.FloatingField('username'),
            bootstrap5.FloatingField('email'),
            bootstrap5.FloatingField('first_name'),
            bootstrap5.FloatingField('last_name'),
        )

    def clean_username(self, *args, **kwargs) -> str:
        username = self.cleaned_data['username']
        if username != self.initial['username']:
            try:
                get_user_model().objects.get(username=username)
            except get_user_model().DoesNotExist:
                return username
            except db.IntegrityError as e:
                error_message = e.__cause__
                logger.error(error_message)
            self.valid = False
            self.add_error('username', 'Error, That username already exists!')
        return username

    def clean_email(self) -> str:
        email = self.cleaned_data['email']
        if email != self.initial['email']:
            try:
                get_user_model().User.objects.get(email=email)
            except get_user_model().User.DoesNotExist:
                return email
            except db.IntegrityError as e:
                error_message = e.__cause__
                logger.error(error_message)
            self.valid = False
            self.add_error('email', 'Error! That email already exists!')
        return email

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']


class Profile(forms.ModelForm):
    class Meta:
        model = profile_models.Profile
        fields = ['profile_user',]
        exclude = ['profile_user']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = helper.FormHelper()
        self.helper.css_class = ''
        self.helper.form_tag = False
