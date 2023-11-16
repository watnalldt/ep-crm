from django.views.generic import TemplateView

from core.views import HTMLTitleMixin


class HomePageView(HTMLTitleMixin, TemplateView):
    template_name = "pages/index.html"
    html_title = "Effectively Managing Energy Solutions"


class SeamlessUtilitiesView(HTMLTitleMixin, TemplateView):
    template_name = "pages/seamless_utilities.html"
    html_title = "Energy Portfolio Seamless Utilities"


class PartnersView(HTMLTitleMixin, TemplateView):
    template_name = "pages/our_partners.html"
    html_title = "Energy Portfolio Our Partners"


class OurServicesView(HTMLTitleMixin, TemplateView):
    template_name = "pages/our_services.html"
    html_title = "Energy Portfolio Our Services"


class ComplaintsPolicyView(HTMLTitleMixin, TemplateView):
    template_name = "pages/complaints_policy.html"
    html_title = "EP Complaints Policy"


class PrivacyPolicyView(HTMLTitleMixin, TemplateView):
    template_name = "pages/privacy_policy.html"
    html_title = "EP Privacy Policy"
