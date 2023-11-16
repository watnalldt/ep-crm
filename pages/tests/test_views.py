import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.urls import reverse

from pages.views import (
    ComplaintsPolicyView,
    HomePageView,
    OurServicesView,
    PartnersView,
    PrivacyPolicyView,
    SeamlessUtilitiesView,
)


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


@pytest.mark.django_db
def test_seamless_utilities_view():
    request = RequestFactory().get(reverse("pages:seamless_utilities"))
    request.user = AnonymousUser()
    view = SeamlessUtilitiesView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert "pages/seamless_utilities.html" in ["pages/seamless_utilities.html"]
    assert "html_title" in response.context_data
    assert response.context_data["html_title"] == "Energy Portfolio Seamless Utilities"


@pytest.mark.django_db
def test_our_partners_view():
    request = RequestFactory().get(reverse("pages:our_partners"))
    request.user = AnonymousUser()
    view = PartnersView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert "pages/our_partners.html" in ["pages/our_partners.html"]
    assert "html_title" in response.context_data
    assert response.context_data["html_title"] == "Energy Portfolio Our Partners"


@pytest.mark.django_db
def test_our_services_view():
    request = RequestFactory().get(reverse("pages:our_services"))
    request.user = AnonymousUser()
    view = OurServicesView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert "pages/our_services.html" in ["pages/our_services.html"]
    assert "html_title" in response.context_data
    assert response.context_data["html_title"] == "Energy Portfolio Our Services"


@pytest.mark.django_db
def test_complaints_policy_view():
    request = RequestFactory().get(reverse("pages:complaints_policy"))
    request.user = AnonymousUser()
    view = ComplaintsPolicyView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert "pages/complaints_policy.html" in ["pages/complaints_policy.html"]
    assert "html_title" in response.context_data
    assert response.context_data["html_title"] == "EP Complaints Policy"


@pytest.mark.django_db
def test_privacy_policy_view():
    request = RequestFactory().get(reverse("pages:privacy_policy"))
    request.user = AnonymousUser()
    view = PrivacyPolicyView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert "pages/privacy_policy.html" in ["pages/privacy_policy.html"]
    assert "html_title" in response.context_data
    assert response.context_data["html_title"] == "EP Privacy Policy"
