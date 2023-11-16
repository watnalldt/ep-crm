from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
import pytest
from .views import HomePageView


@pytest.mark.django_db
def test_returns_200_status_code():
    request = RequestFactory().get(reverse("pages:home"))
    request.user = AnonymousUser()
    view = HomePageView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert 'pages/index.html' in ['pages/index.html']
    assert "html_title" in response.context_data
    assert response.context_data["html_title"] == "Effectively Managing Energy Solutions"

