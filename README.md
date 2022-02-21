# django_profile
a django app that provides basic profile functionality, as a foundation for other apps.  It adds a profile model to a user using a signal, and provides templates via django-crispy-forms that show the profile form and the user auth forms from the django_users app https://github.com/millerthegorilla/django_users that is a dependency of this app.  It adds a field, `display_name`, to the user auth form.  Validation uses fuzzy logic provided by the python app fuzzywuzzy, and crispy-forms uses the bootstrap5 template for layout/theming.

## install
pip install git+https://github.com/millerthegorilla/safe_imagefield.git#egg=safe_imagefield

## settings
You will need to set the site domain in the admin app, and also the settings.BASE_HTML for the statement `{% extends BASE_HTML %}` in the templates where BASE_HTML comes from the context_processor.

## dependencies
git+https://github.com/millerthegorilla/safe_imagefield.git#egg=safe_imagefield
django-crispy-forms==1.11.2
crispy-bootstrap==5 0.6
fuzzywuzzy==0.18.0
django-recaptcha==2.0.6