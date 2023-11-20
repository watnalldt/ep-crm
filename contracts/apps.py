from django.apps import AppConfig
from watson import search


class ContractsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "contracts"

    def ready(self):
        contract = self.get_model("Contract")
        search.register(
            contract,
            fields=[
                "client__client",
                "business_name",
                "site_address",
                "mpan_mpr",
                "meter_serial_number",
            ],
        )
