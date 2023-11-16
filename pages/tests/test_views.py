import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.urls import reverse

from pages.views import HomePageView, SeamlessUtilitiesView


@pytest.mark.django_db
def test_home_page_view():
    request = RequestFactory().get(reverse("pages:home"))
    request.user = AnonymousUser()
    view = HomePageView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert "pages/index.html" in ["pages/index.html"]
    assert "html_title" in response.context_data
    assert response.context_data["html_title"] == "Effectively Managing Energy Solutions"


def seamless_utilities_view():
    request = RequestFactory().get(reverse("pages:seamless_utilities"))
    request.user = AnonymousUser()
    view = SeamlessUtilitiesView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert "pages/seamless_utilities.html" in ["pages/seamless_utilities.html"]
    assert "html_title" in response.context_data
    assert response.context_data["html_title"] == "Energy Portfolio Seamless Utilities"
