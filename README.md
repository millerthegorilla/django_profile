# django_profile
a django app that provides basic profile functionality, as a foundation for other apps.  It adds a profile model to a user using a signal, and provides templates via django-crispy-forms that show the profile form and the user auth forms from the django_users app https://github.com/millerthegorilla/django_users that is a dependency of this app.  It adds a field, `display_name`, to the user auth form.  Validation uses fuzzy logic provided by the python app fuzzywuzzy, and crispy-forms uses the bootstrap5 template for layout/theming.

## install
pip install git+https://github.com/millerthegorilla/django_profile.git#egg=django_profile
add django_profile to your installed apps.
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    'django_profile',
]
```
## settings
You will need to set the site domain in the admin app, and also the settings.BASE_HTML for the statement `{% extends BASE_HTML %}` in the templates where BASE_HTML comes from the context_processor.

You will also need recaptcha settings...
```
## RECAPTCHA SETTINGS
RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
```
The keys shown here are the test keys that allow you to use the recaptcha in your development setup.  The silenced system check simply silences the warning that is displayed that says that the recaptcha keys are the test keys.

And crispy-forms bootstrap5 has some settings...
```
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```
Finally, you can make the app abstract if you are subclassing it in another app.
```
ABSTRACTPROFILE = True
```


## dependencies
git+https://github.com/millerthegorilla/django_users.git#egg=django_users
django-crispy-forms==1.11.2
crispy-bootstrap==5 0.6
fuzzywuzzy==0.18.0
django-recaptcha==2.0.6