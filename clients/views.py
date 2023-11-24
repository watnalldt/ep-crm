from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView, ListView

from contracts.models import Contract
from core.decorators import account_manager_required
from core.views import HTMLTitleMixin

from .forms import MeterForm
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


# return all clients and associated contracts
class ClientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Client
    context_object_name = "all_clients"
    template_name = "clients/contracts/all_contracts/all_clients.html"

    def test_func(self):
        return self.request.user.groups.filter(name="Account Managers").exists()


class AllClientsView(LoginRequiredMixin, UserPassesTestMixin, HTMLTitleMixin, DetailView):
    queryset = Client.objects.all()
    template_name = "clients/contracts/all_contracts/all_client_contracts.html"

    def get_html_title(self):
        return self.object.client

    def test_func(self):
        return self.request.user.groups.filter(name="Account Managers").exists()


class AllContractsDetailView(LoginRequiredMixin, UserPassesTestMixin, HTMLTitleMixin, DetailView):
    model = Contract
    template_name = "clients/contracts/all_contracts/all_contracts_detail.html"

    def get_html_title(self):
        return self.object.business_name

    def test_func(self):
        return self.request.user.groups.filter(name="Account Managers").exists()


def meter_reading(request, pk):
    # pk = kwargs.get("pk")
    contracts = get_object_or_404(Contract, pk=pk, client_manager=request.user.id)

    if request.method == "POST":
        form = MeterForm(request.POST, request.FILES)

        if form.is_valid():
            subject = "Meter Reading"
            data = {
                "from_email": form.cleaned_data["from_email"],
                "client_name": form.cleaned_data["client_name"],
                "site_address": form.cleaned_data["site_address"],
                "mpan_mpr": form.cleaned_data["mpan_mpr"],
                "meter_serial_number": form.cleaned_data["meter_serial_number"],
                "utility_type": form.cleaned_data["utility_type"],
                "supplier": form.cleaned_data["supplier"],
                "meter_reading": form.cleaned_data["meter_reading"],
                "meter_reading_date": form.cleaned_data["meter_reading_date"],
                "supplier_meter_email": contracts.supplier.meter_email,
            }

            message = get_template("clients/contracts/meter_reading_submission.html").render(data)
            try:
                mail = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    ["josh@energyportfolio.co.uk", data["supplier_meter_email"]],
                )
                if "attachment" in request.FILES:
                    attachment = request.FILES.get("attachment")
                    mail.attach(attachment.name, attachment.read(), attachment.content_type)
                    mail.content_subtype = "html"
                    mail.send()
                else:
                    mail.content_subtype = "html"
                    mail.send()

            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            messages.success(request, "Your meter reading has been received.")
            return redirect("users:my_account")
    form = MeterForm(
        initial={
            "from_email": request.user.email,
            "client_name": contracts.client,
            "site_address": contracts.site_address,
            "mpan_mpr": contracts.mpan_mpr,
            "meter_serial_number": contracts.meter_serial_number,
            "utility_type": contracts.utility,
            "supplier": contracts.supplier,
        }
    )
    return render(
        request,
        "client_managers/meter_reading.html",
        {"form": form, "contract": contracts},
    )
