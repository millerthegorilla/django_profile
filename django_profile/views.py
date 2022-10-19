from django import http, shortcuts, urls
from django.contrib import auth
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

    def populate_initial_user_form(self):
        return {
            "username": self.request.user.username,
            "email": self.request.user.email,
            "first_name": self.request.user.first_name,
            "last_name": self.request.user.last_name,
        }

    def get_context_data(self, **kwargs) -> dict:
        user_form = self.user_form_class(initial=self.populate_initial_user_form())
        form = self.form_class({"profile_user": self.request.user})
        return {"form": form, "user_form": user_form}

    def post(self, request: http.HttpRequest):
        form = self.form_class(request.POST, initial=request.user.profile.__dict__)
        user_form = self.user_form_class(
            request.POST, initial=self.populate_initial_user_form()
        )
        if len(user_form["username"].errors):
            user_form.errors["username"][:] = (
                value
                for value in user_form.errors["username"]
                if value != "A user with that username already exists."
            )
            if not len(user_form.errors["username"]):
                del user_form.errors["username"]

        if not form.errors and form.fields:
            fm = form.save(commit=False)
            fm.profile_user = request.user
            fm.save()
        if not user_form.errors:
            uf = user_form.save(commit=False)
            uf.id = request.user.id
            uf.save(update_fields=[x for x in user_form.cleaned_data.keys()])
        if user_form.errors or form.errors:
            return shortcuts.render(
                request,
                self.template_name,
                context={"form": form, "user_form": user_form},
            )

        return shortcuts.redirect(self.success_url)
