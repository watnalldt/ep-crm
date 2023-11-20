from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control, never_cache
from django.views.generic import ListView, TemplateView

from clients.models import Client
from contracts.models import Contract
from core.decorators import account_manager_required
from core.views import HTMLTitleMixin

from .utils import detect_user


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("users:my_account")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd["username"], password=cd["password"])

            if user is not None:
                auth.login(request, user)
                messages.success(request, " You are logged in..")
                return redirect("users:my_account")
            else:
                messages.error(request, "Invalid login credentials..")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


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


@method_decorator([never_cache, account_manager_required], name="dispatch")
class ContractSearchView(LoginRequiredMixin, ListView):
    model = Contract
    template_name = "account_managers/search_results.html"
    context_object_name = "results"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return self.search_contracts(query)
        else:
            return Contract.objects.all()

    def search_contracts(self, query):
        return Contract.objects.filter(
            Q(mpan_mpr__isnull=True)
            | Q(mpan_mpr__icontains=query)
            | Q(client__client__icontains=query)
            | Q(business_name__icontains=query)
            | Q(site_address__icontains=query)
        )
