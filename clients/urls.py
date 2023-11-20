from django.urls import path

from . import views

app_name = "clients"

urlpatterns = [
    path(
        "client_contracts/<int:pk>/",
        views.ClientDetailView.as_view(),
        name="client_contracts",
    ),
    path(
        "contract_detail/<int:pk>/",
        views.ContractDetailView.as_view(),
        name="contract_detail",
    ),
    # Urls for all clients and associated contracts
    path("all_clients/", views.ClientListView.as_view(), name="all_clients"),
    path(
        "all_client_contracts/<int:pk>/",
        views.AllClientsView.as_view(),
        name="all_client_contracts",
    ),
    path(
        "all_clients_contract_detail/<int:pk>/",
        views.AllContractsDetailView.as_view(),
        name="all_clients_contract_detail",
    ),
]
