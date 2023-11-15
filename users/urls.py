from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    # Dashboards
    path("my_account/", views.my_account, name="my_account"),
    path(
        "account_managers_dashboard",
        views.AccountManagerView.as_view(),
        name="account_managers_dashboard",
    ),
    # Client List
    path(
        "account_managers_client_list",
        views.AccountManagerClientList.as_view(),
        name="client_list",
    ),
]
