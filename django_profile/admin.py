from django import conf
from django.contrib import admin
from . import models as profile_models

# Register your models here.


if not conf.settings.ABSTRACTPROFILE:
    @admin.register(profile_models.Profile)
    class ProfileAdmin(admin.ModelAdmin):
        list_display = ['profile_user']
        list_filter = ['profile_user']
        search_fields = ['profile_user']
