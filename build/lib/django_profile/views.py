from django import http, shortcuts, urls
from django.contrib.auth import mixins
from django.views import generic

from . import forms as profile_forms
from . import models as profile_models


class ProfileUpdate(mixins.LoginRequiredMixin, generic.edit.UpdateView):
    form_class = profile_forms.Profile
    user_form_class = profile_forms.UserProfile
    model = profile_models.Profile
    success_url = urls.reverse_lazy("django_profile:profile_update_view")
    template_name = "django_profile/profile_update_form.html"

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        context = self.get_context_data()
        return shortcuts.render(request, self.template_name, context)

    def get_object(self) -> profile_models.Profile:
        return self.model.objects.get(profile_user_id=self.request.user.id)

    def populate_initial_user_form(self, user):
        return {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

    def get_context_data(self, **kwargs) -> dict:
        user_form = self.user_form_class(
            initial=self.populate_initial_user_form(self.request.user)
        )
        form = self.form_class()
        form.initial = {"profile_user": self.request.user}
        return {"form": form, "user_form": user_form}

    def post(self, request: http.HttpRequest):
        user_form = self.user_form_class(request.POST)
        user_form.initial.update(self.populate_initial_user_form(request.user))
        user_form.is_valid()
        try:
            user_form.errors.pop("username")
        except KeyError:
            pass
        # next two lines not really necessary unless view is subclassed
        form = self.form_class(request.POST)
        form.is_valid()
        if len(user_form.errors) or len(form.errors):
            return shortcuts.render(
                request,
                self.template_name,
                context={"form": form, "user_form": user_form},
            )
        if len(user_form.changed_data):
            user = auth.get_user_model().objects.get(
                username=user_form.initial["username"]
            )
            for change in user_form.changed_data:
                setattr(user, change, user_form[change].value())
            user.save(update_fields=user_form.changed_data)
        # currently profile doesn't have anything that can be changed,
        # but the view may be subclassed
        if len(form.changed_data):
            profile = self.model.objects.get(profile_user=request.user)
            for change in form.changed_data:
                setattr(profile, change, form[change].value())
            profile.save(update_fields=form.changed_data)

        return shortcuts.redirect(self.success_url)
