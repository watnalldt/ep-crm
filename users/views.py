from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control, never_cache
from django.views.generic import ListView, TemplateView

from clients.models import Client
from core.decorators import account_manager_required
from core.views import HTMLTitleMixin

from .utils import detect_user


def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "You have successfully logged out.")
    return redirect("users:login")


@login_required(login_url="users:login")  # login required decorators
#  Function For MyAccount.
def my_account(request):
    user = request.user
    redirect_url = detect_user(user)
    return redirect(redirect_url)


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
