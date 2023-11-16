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
]
