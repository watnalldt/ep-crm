from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView

from contracts.models import Contract
from core.decorators import account_manager_required
from core.views import HTMLTitleMixin

from .models import Client


@method_decorator([account_manager_required, never_cache], name="dispatch")
class ClientDetailView(LoginRequiredMixin, HTMLTitleMixin, DetailView):
    """Details all contracts for that client by account manager"""

    model = Client
    template_name = "clients/contracts/client_detail.html"
    login_url = "/users/login/"

    def get_html_title(self):
        return self.object.client

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Client.objects.filter(account_manager=self.request.user)
        else:
            return Client.objects.none()


@method_decorator([never_cache, account_manager_required], name="dispatch")
class ContractDetailView(LoginRequiredMixin, HTMLTitleMixin, DetailView):
    """Details individual contracts for that client by client manager"""

    model = Contract

    template_name = "clients/contracts/contract_detail.html"
    login_url = "/users/login/"

    def get_html_title(self):
        return self.object.business_name

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Contract.objects.filter(client__account_manager=self.request.user)
        else:
            return Contract.objects.none()
