# test_html_title_mixin.py

import pytest

from .views import HTMLTitleMixin


class MockView(HTMLTitleMixin):
    html_title = "Test Title"
    html_title_prefix = "Prefix "
    html_title_suffix = " Suffix"
    html_title_required = True


def test_generate_html_title():
    view = MockView()
    html_title = view.generate_html_title()
    assert html_title == "Prefix Test Title Suffix"


def test_generate_html_title_missing_required():
    view = MockView()
    view.html_title_required = False
    html_title = view.generate_html_title()
    assert html_title == "Prefix Test Title Suffix"


def test_generate_html_title_missing_title():
    view = MockView()
    view.html_title = ""
    with pytest.raises(ValueError, match="HTMLTitleMixin requires an html_title"):
        view.generate_html_title()


def test_get_context_data():
    view = MockView()
    context = view.get_context_data()
    assert "html_title" in context
    assert context["html_title"] == "Prefix Test Title Suffix"
