from django.views.generic import TemplateView

from core.views import HTMLTitleMixin


class HomePageView(HTMLTitleMixin, TemplateView):
    template_name = "pages/index.html"
    html_title = "Effectively Managing Energy Solutions"


class SeamlessUtilitiesView(HTMLTitleMixin, TemplateView):
    template_name = "pages/seamless_utilities.html"
    html_title = "Energy Portfolio Seamless Utilities"
