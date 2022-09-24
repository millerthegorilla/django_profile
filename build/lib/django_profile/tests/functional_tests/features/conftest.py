import os

import pytest
from django.urls import reverse

PROFILE_URL = reverse("django_profile:profile_update_view")

PAGES_DICT = {
    "profile": PROFILE_URL,
}


@pytest.fixture()
def browser(sb, live_server, settings):
    staging_server = os.environ.get("STAGING_SERVER")
    if staging_server:
        sb.visit(staging_server)
    else:
        sb.visit(live_server)
    sb.domain = sb.get_domain_url(sb.get_current_url())
    sb.pages = PAGES_DICT
    return sb


@pytest.fixture()
def profile_page(browser):
    browser.visit(browser.domain + PROFILE_URL)
    return browser
