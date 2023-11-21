from datetime import timedelta

from django import template
from django.utils import timezone

from clients.models import Client
from contracts.models import Contract

register = template.Library()

current_date = timezone.now()
end_date_30_days = current_date + timedelta(days=30)
end_date_60_days = current_date + timedelta(days=60)


@register.simple_tag
def total_contracts(user):
    """Returns total number of contracts for the given client"""
    contracts = Contract.objects.filter(client__account_manager=user).count()
    return contracts


@register.simple_tag
def total_clients(user):
    """Returns total number of clients for the given user"""
    clients = Client.objects.filter(account_manager=user).count()
    return clients


@register.simple_tag
def total_seamless_contracts(user):
    """Returns most 5 most recent events"""
    contracts = (
        Contract.objects.filter(client__account_manager=user)
        .filter(contract_type="SEAMLESS")
        .count()
    )
    return contracts


@register.simple_tag
def total_non_seamless_contracts(user):
    """Returns most 5 most recent events"""
    contracts = (
        Contract.objects.filter(client__account_manager=user)
        .filter(contract_type="NON_SEAMLESS")
        .count()
    )
    return contracts


@register.simple_tag
def total_contracts_directors_approval(user):
    """Returns most 5 most recent events"""
    contracts = (
        Contract.objects.filter(client__account_manager=user)
        .filter(is_directors_approval="YES")
        .count()
    )
    return contracts


@register.simple_tag
def utility_gas_contracts(user):
    gas_contracts = (
        Contract.objects.filter(client__account_manager=user).filter(utility__utility="Gas").count()
    )
    return gas_contracts


@register.simple_tag
def utility_electricity_contracts(user):
    electricity_contracts = (
        Contract.objects.filter(client__account_manager=user)
        .filter(utility__utility="Electricity")
        .count()
    )
    return electricity_contracts


@register.simple_tag
def electricity_hh_contracts(user):
    hh_contracts = (
        Contract.objects.filter(client__account_manager=user)
        .filter(utility__utility="Electricity - HH")
        .count()
    )
    return hh_contracts


@register.simple_tag
def electricity_nhh_contracts(user):
    nhh_contracts = (
        Contract.objects.filter(client__account_manager=user)
        .filter(utility__utility="Electricity - NHH")
        .count()
    )
    return nhh_contracts


@register.simple_tag
def electricity_ums_contracts(user):
    ums_contracts = (
        Contract.objects.filter(client__account_manager=user)
        .filter(utility__utility="Electricity - UMS")
        .count()
    )
    return ums_contracts


@register.simple_tag
def corona_supplier_contracts(user):
    corona_contracts = (
        Contract.objects.filter(client__account_manager=user)
        .filter(supplier__supplier="Corona")
        .count()
    )
    return corona_contracts


@register.simple_tag
def crown_supplier_contracts(user):
    crown_contracts = (
        Contract.objects.filter(client__account_manager=user)
        .filter(supplier__supplier="Crown")
        .count()
    )
    return crown_contracts


@register.simple_tag
def sse_supplier_contracts(user):
    sse_contracts = (
        Contract.objects.filter(client__account_manager=user)
        .filter(supplier__supplier="SSE")
        .count()
    )
    return sse_contracts


@register.simple_tag
def pozitive_supplier_contracts(user):
    pozitive_contracts = (
        Contract.objects.filter(client__account_manager=user)
        .filter(supplier__supplier="Pozitive")
        .count()
    )
    return pozitive_contracts


@register.simple_tag
def eon_supplier_contracts(user):
    eon_contracts = (
        Contract.objects.filter(client__account_manager=user)
        .filter(supplier__supplier="E.ON")
        .count()
    )
    return eon_contracts


@register.simple_tag
def contracts_expiring_30_days(user):
    expiry_30_days = (
        Contract.objects.filter(client__account_manager=user)
        .filter(contract_end_date__lte=end_date_30_days)
        .count()
    )
    return expiry_30_days


@register.simple_tag
def contracts_expiring_60_days(user):
    expiry_60_days = (
        Contract.objects.filter(client__account_manager=user)
        .filter(contract_end_date__gte=end_date_30_days)
        .filter(contract_end_date__lte=end_date_60_days)
        .count()
    )
    return expiry_60_days


@register.simple_tag
def contracts_expiring_over_60_days(user):
    expiry_over_60_days = (
        Contract.objects.filter(client__account_manager=user)
        .filter(contract_end_date__gt=end_date_60_days)
        .count()
    )
    return expiry_over_60_days


@register.simple_tag
def live_contracts(user):
    contracts = (
        Contract.objects.filter(client__account_manager=user).filter(contract_status="LIVE").count()
    )
    return contracts


@register.simple_tag
def out_of_contract(user):
    ooc = Contract.objects.filter(client__account_manager=user).filter(is_ooc="YES").count()
    return ooc


@register.simple_tag
def under_objection(user):
    objection = (
        Contract.objects.filter(client__account_manager=user)
        .filter(contract_status="OBJECTION")
        .count()
    )
    return objection


@register.simple_tag
def pricing(user):
    pricing_contract = (
        Contract.objects.filter(client__account_manager=user)
        .filter(contract_status="PRICING")
        .count()
    )
    return pricing_contract


@register.simple_tag
def locked(user):
    locked_contract = (
        Contract.objects.filter(client__account_manager=user)
        .filter(contract_status="LOCKED")
        .count()
    )
    return locked_contract


@register.simple_tag
def directors_approval(user):
    approval_required = (
        Contract.objects.filter(client__account_manager=user)
        .filter(is_directors_approval="YES")
        .count()
    )
    return approval_required
