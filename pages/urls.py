from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path(
        "seamless-utilities",
        views.SeamlessUtilitiesView.as_view(),
        name="seamless_utilities",
    ),
    path("our-partners", views.PartnersView.as_view(), name="our_partners"),
    path("our-services", views.OurServicesView.as_view(), name="our_services"),
    path(
        "complaints-policy",
        views.ComplaintsPolicyView.as_view(),
        name="complaints_policy",
    ),
    path("privacy-policy", views.PrivacyPolicyView.as_view(), name="privacy_policy"),
]
