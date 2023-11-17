from django.urls import path

from . import views

app_name = "clients"

urlpatterns = [
    path(
        "client_contracts/<int:pk>/",
        views.ClientDetailView.as_view(),
        name="client_contracts",
    ),
    ]
