import typing

from django import shortcuts, forms, urls, http
from django.views import generic
from django.contrib import auth
#from django.contrib.auth import mixins
from django.template import defaultfilters

import django_users.views as users_views

from . import custom_registration
from . import models as profile_models
from . import forms as profile_forms


class ProfileUpdate(auth.mixins.LoginRequiredMixin, generic.edit.UpdateView):
    form_class = profile_forms.Profile
    user_form_class = profile_forms.UserProfile
    model = profile_models.Profile
    success_url = urls.reverse_lazy('django_profile:profile_update_view')
    template_name = 'django_profile/profile_update_form.html'

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        self.object = self.get_object()
        context = self.get_context_data()
        return shortcuts.render(request, self.template_name, context)

    def get_object(self) -> profile_models.Profile:
        return self.model.objects.get(profile_user_id=self.request.user.id)

    def populate_initial(self, user):
        return {
                    'username': self.request.user.username, # type: ignore
                    'email': self.request.user.email,
                    'first_name': self.request.user.first_name,
                    'last_name': self.request.user.last_name
                }

    def get_context_data(self, *args, **kwargs) -> dict:
        user_form = self.user_form_class()
        user_form.initial = self.populate_initial(self.request.user)
        form = self.form_class()
        form.initial = { 'profile_user': self.request.user }
        return {'form': form, 'user_form': user_form }

    def post(self, request:http.HttpRequest):
        user_form = self.user_form_class(self.request.POST)
        user_form.initial = {'username': self.request.user.username, # type: ignore
                             'email': self.request.user.email,
                             'first_name': self.request.user.first_name,
                             'last_name': self.request.user.last_name}
        user_form.is_valid()
        try:
            user_form.errors.pop('username')
        except KeyError:
            pass
        # next two lines not really necessary
        form = self.form_class(self.request.POST)
        form.is_valid()
        if len(user_form.errors) or len(form.errors):
            return shortcuts.render(
                self.request,
                self.template_name,
                context={
                    'form': form,
                    'user_form': user_form})
        if len(user_form.changed_data):
            breakpoint()
            user = auth.get_user_model().objects.get(username=user_form['username'].value())
            for change in user_form.changed_data:
                setattr(user,change,user_form[change].value())
            user.save(update_fields=user_form.changed_data)
        #currently profile doesn't have anything that can be changed, but just in case for laters...
        if len(form.changed_data):
            profile = self.model.objects.get(profile_user=request.user)
            for change in form.changed_data:
                setattr(profile,change,form[change].value())
            profile.save(update_fields=form.changed_data)
        # for change in user_form.changed_data:
        #     setattr(self.request.user, change, user_form[change].value())
        # self.request.user.save()

        return shortcuts.redirect(self.success_url)
    # def form_valid(self, form: forms.ModelForm) -> typing.Union[http.HttpResponse, http.HttpResponseRedirect]: 
    #     user_form = self.user_form_class(self.request.POST)
    #     user_form.initial = {'username': self.request.user.username, # type: ignore
    #                          'email': self.request.user.email,
    #                          'first_name': self.request.user.first_name,
    #                          'last_name': self.request.user.last_name}
    #     # django validates username against database automatically, but not email
    #     # so I clear the errors from the database as my form is validating the username
    #     # independently of the database validation.
    #     # the is_valid function then populates errors.
    #     # there is probably a saner way to have two forms coexisting on the same page,
    #     # but its early days.
    #     user_form.errors.clear()
    #     user_form.is_valid()
    #     try:
    #         user_form.errors.pop('username')
    #     except KeyError:
    #         pass
    #     if len(user_form.errors):
    #         return shortcuts.render(
    #             self.request,
    #             self.template_name,
    #             context={
    #                 'form': form,
    #                 'user_form': user_form})
    #     for change in user_form.changed_data:
    #         setattr(self.request.user, change, user_form[change].value())
    #     self.request.user.save()
    #     return shortcuts.render(self.request, self.template_name, {'form': form,
    #     'user_form': user_form})

    # def form_invalid(self, form, **kwargs):
    #     user_form = self.user_form_class(self.request.POST)
    #     user_form.initial = {'username': self.request.user.username, # type: ignore
    #                          'email': self.request.user.email,
    #                          'first_name': self.request.user.first_name,
    #                          'last_name': self.request.user.last_name}
    #     user_form.errors.pop('username')
    #     return shortcuts.render(self.request, self.template_name, { 'form' : form, 'user_form': user_form })


# NEEDED FOR ADDITION OF DISPLAY_NAME
# the following goes in the project top level urls.py
# from django_profile.views import CustomRegister
# path('users/accounts/register/', CustomRegister.as_view(), name='register'),
class CustomRegister(users_views.Register):
    form_class = custom_registration.CustomUserCreation

    def form_valid(self, form: forms.ModelForm) -> http.HttpResponseRedirect:
        user = form.save()
        user.profile.display_name = defaultfilters.slugify(form['display_name'].value())
        user.profile.save(update_fields=['display_name'])
        super().form_valid(form, user)
        return shortcuts.redirect('password_reset_done')
