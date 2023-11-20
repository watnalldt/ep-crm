from datetime import date

from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from clients.models import Client
from utilities.models import Supplier, Utility


class ContractsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("client", "supplier", "utility")


class UtilityQuerySet(models.QuerySet):
    """Returns contracts base on either gas or electricity"""

    def gas(self):
        return self.filter(utility__utility="Gas").prefetch_related("client", "supplier", "utility")

    def electricity(self):
        return self.filter(utility__utility="Electricity").prefetch_related(
            "client", "supplier", "utility"
        )


class ContractTypeQuerySet(models.QuerySet):
    """Returns contracts based on either  seamless or non-seamless"""

    def seamless(self):
        return self.filter(contract_type="SEAMLESS").prefetch_related(
            "client", "supplier", "utility"
        )

    def non_seamless(self):
        return self.filter(contract_type="NON-SEAMLESS").prefetch_related(
            "client", "supplier", "utility"
        )


class Contract(models.Model):
    class ContractType(models.TextChoices):
        """Determines if the contract is seamless or non-seamless. Defaults to seamless"""

        SEAMLESS = "SEAMLESS", _("Seamless")
        NON_SEAMLESS = "NON_SEAMLESS", _("Non-Seamless")

    class ContractStatus(models.TextChoices):
        """Determines if status of the contract is live or removed. Defaults to live"""

        LIVE = "LIVE", _("Live")
        REMOVED = "REMOVED", _("Removed")
        LOCKED = "LOCKED", _("Locked")
        PRICING = "PRICING", _("Pricing")
        OBJECTION = "OBJECTION", _("Objection")
        NEW = "NEW", _("New")

    class OutOfContract(models.TextChoices):
        """The default is set to No

        This field is taken from those contracts that
        are designated as out of contract in the master spreadsheets.
        It does not depend on the contract end date
        """

        YES = "YES", _("Yes")
        NO = "NO", _("No")

    class DirectorsApproval(models.TextChoices):
        """The default is set to No"""

        YES = "YES", _("Yes")
        NO = "NO", _("No")

    class VatDeclaration(models.TextChoices):
        """The default is set to No"""

        YES = "YES", _("Yes")
        NO = "NO", _("No")

    contract_type = models.CharField(
        max_length=20, choices=ContractType.choices, default=ContractType.SEAMLESS
    )
    contract_status = models.CharField(
        max_length=20, choices=ContractStatus.choices, default=ContractStatus.LIVE
    )

    dwellent_id = models.CharField(
        verbose_name="Dwellent ID", max_length=100, null=True, blank=True
    )
    bid_id = models.CharField(verbose_name="BID ID", max_length=100, null=True, blank=True)
    portal_status = models.CharField(
        verbose_name="Portal Status", max_length=255, null=True, blank=True
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="Client Name",
        related_name="client_contracts",
    )
    is_directors_approval = models.CharField(
        verbose_name="Directors Approval",
        choices=DirectorsApproval.choices,
        default=DirectorsApproval.NO,
    )
    business_name = models.CharField(verbose_name="Business Name", max_length=255)
    company_reg_number = models.CharField(
        verbose_name="Company Reg Number", max_length=250, null=True, blank=True
    )
    utility = models.ForeignKey(
        Utility,
        on_delete=models.CASCADE,
        verbose_name="Utility Type",
        related_name="contract_utilities",
    )
    top_line = models.CharField(verbose_name="Top Line", max_length=40, null=True, blank=True)
    mpan_mpr = models.CharField(verbose_name="MPAN/MPR", max_length=255)
    meter_serial_number = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text=mark_safe(
            "<a href='https://www.ecoes.co.uk' target='_blank'>" "Look up Meter Serial Number</a>"
        ),
    )
    building_name = models.CharField(
        verbose_name="Building Name", max_length=255, null=True, blank=True
    )
    site_address = models.TextField(verbose_name="Site Address", null=True, blank=True)
    billing_address = models.CharField(
        verbose_name="Billing Address", max_length=255, null=True, blank=True
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        verbose_name="Supplier Name",
        related_name="contract_suppliers",
    )
    reference_4 = models.CharField(max_length=50, null=True, blank=True)
    contract_start_date = models.DateField(
        verbose_name="Contract Start Date", null=True, blank=True
    )
    contract_end_date = models.DateField(verbose_name="Contract End Date", null=True, blank=True)
    supplier_start_date = models.DateField(
        verbose_name="Supplier Start Date", null=True, blank=True
    )
    account_number = models.CharField(
        verbose_name="Account Number", max_length=100, null=True, blank=True
    )
    eac = models.FloatField(verbose_name="EAC", null=True, blank=True)
    day_consumption = models.FloatField(verbose_name="Day Consumption", null=True, blank=True)
    night_consumption = models.FloatField(verbose_name="Night Consumption", null=True, blank=True)
    kva = models.CharField(verbose_name="KVA", max_length=15, null=True, blank=True)
    vat = models.CharField(verbose_name="VAT", max_length=100, null=True, blank=True)
    contract_value = models.DecimalField(
        verbose_name="Contract Value",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    standing_charge = models.DecimalField(
        verbose_name="Standing Charge",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )
    sc_frequency = models.CharField(
        verbose_name="Standing Charge Frequency", max_length=250, null=True, blank=True
    )
    unit_rate_1 = models.DecimalField(
        verbose_name="Unit Rate 1",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )
    unit_rate_2 = models.DecimalField(
        verbose_name="Unit Rate 2",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )
    unit_rate_3 = models.DecimalField(
        verbose_name="Unit Rate 3",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )
    feed_in_tariff = models.DecimalField(
        verbose_name="Feed In Tariff",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )
    seamless_status = models.CharField(
        verbose_name="Seamless Status", max_length=50, null=True, blank=True
    )
    profile = models.CharField(verbose_name="Profile", max_length=100, null=True, blank=True)
    is_ooc = models.CharField(
        verbose_name="Out Of Contract", choices=OutOfContract.choices, default=OutOfContract.NO
    )
    service_type = models.CharField(max_length=50, null=True, blank=True)

    pence_per_kilowatt = models.DecimalField(
        verbose_name="Pence Per Kilowatt",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )
    day_kilowatt_hour_rate = models.DecimalField(
        verbose_name="Day Kilowatt Hour Rate",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )
    night_rate = models.DecimalField(
        verbose_name="Night Rate", max_digits=8, decimal_places=8, null=True, blank=True
    )
    annualised_budget = models.DecimalField(
        verbose_name="Annualised Budget",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    commission_per_annum = models.DecimalField(
        verbose_name="Commission Per Annum",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    commission_per_unit = models.DecimalField(
        verbose_name="Commission Per Unit",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    commission_per_contract = models.DecimalField(
        verbose_name="Commission Per Contract",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    partner_commission = models.DecimalField(
        verbose_name="Partner Commission",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    smart_meter = models.CharField(verbose_name="Smart Meter", max_length=50, null=True, blank=True)
    vat_declaration_sent = models.CharField(
        verbose_name="Vat Declaration Sent",
        choices=VatDeclaration.choices,
        default=VatDeclaration.NO,
    )
    vat_declaration_date = models.DateField(verbose_name="Date Sent", blank=True, null=True)

    vat_declaration_expires = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    future_contract_start_date = models.DateField(
        verbose_name="Future Contract Start Date", null=True, blank=True
    )

    future_contract_end_date = models.DateField(
        verbose_name="Future Contract End Date", null=True, blank=True
    )
    future_unit_rate_1 = models.DecimalField(
        verbose_name="Future Unit Rate 1",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )
    future_unit_rate_2 = models.DecimalField(
        verbose_name="Future Unit Rate 2",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )
    future_unit_rate_3 = models.DecimalField(
        verbose_name="Future Unit Rate 3",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )

    future_supplier = models.ForeignKey(
        Supplier,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Future Supplier",
        related_name="future_suppliers",
    )
    future_standing_charge = models.DecimalField(
        verbose_name="Future Standing Charge",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )
    history = HistoricalRecords()

    objects = ContractsManager()  # Default Manager
    utilities = UtilityQuerySet.as_manager()  # Manager returns contracts per utility
    contracts = ContractTypeQuerySet.as_manager()  # Manager returns contract type

    class Meta:
        indexes = [
            models.Index(fields=["mpan_mpr"]),
            models.Index(fields=["client"]),
            models.Index(fields=["-client"]),
            models.Index(fields=["business_name"]),
            models.Index(fields=["-business_name"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["mpan_mpr", "id"],
                name="unique_contract",
            )
        ]
        db_table = "client_contracts"
        verbose_name = _("Client Contract")
        verbose_name_plural = _("Client Contracts")
        ordering = ["contract_end_date"]

    def __str__(self):
        return f"{self.business_name} with mpan {self.mpan_mpr}"

    def save(self, *args, **kwargs):
        if self.vat_declaration_sent == self.VatDeclaration.YES:
            if self.vat_declaration_date is None:
                raise ValueError(
                    "Error: vat_declaration_date cannot be null when vat_declaration_sent is YES."
                )
            # Set vat_declaration_expires to contract_end_date
            self.vat_declaration_expires = self.contract_end_date
        else:
            # If vat_declaration_sent is not YES, set vat_declaration_expires to None
            self.vat_declaration_expires = None

        super().save(*args, **kwargs)

    # Returns the number of days left on the contrac
    @property
    def days_till(self):
        today = date.today()
        days_till = self.contract_end_date - today
        return str(days_till).split(",", 1)[0]
