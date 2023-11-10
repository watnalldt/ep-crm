import reversion
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from core.models import TimeStampedModel


class Utility(TimeStampedModel):
    utility = models.CharField(max_length=25, unique=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Utility")
        verbose_name_plural = _("Utilities")

    def __str__(self):
        return self.utility


@reversion.register
# Add this decorator to enable version control for the model
class Supplier(TimeStampedModel):
    supplier = models.CharField(max_length=100, unique=True)
    meter_email = models.EmailField(null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")

    def __str__(self):
        return self.supplier
