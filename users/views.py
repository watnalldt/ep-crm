from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control, never_cache
from django.views.generic import ListView, TemplateView

from clients.models import Client
from core.decorators import account_manager_required
from core.views import HTMLTitleMixin


@method_decorator([never_cache, account_manager_required], name="dispatch")
class AccountManagerView(LoginRequiredMixin, HTMLTitleMixin, TemplateView):
    # Returns the Account Manager's Dashboard on login.
    model = Client
    template_name = "account_managers/account_managers_dashboard.html"
    html_title = "My Dashboard"


@method_decorator([never_cache, account_manager_required], name="dispatch")
class AccountManagerClientList(LoginRequiredMixin, HTMLTitleMixin, ListView):
    # Lists out all their client's with a link to their respective contracts
    model = Client
    template_name = "account_managers/client_list.html"
    html_title = "Client List"
    login_url = "/users/login/"

    def get_queryset(self):
        return Client.objects.filter(account_manager=self.request.user)
