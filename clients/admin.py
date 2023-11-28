from django.contrib import admin
from django.contrib.auth import get_user_model
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from .models import Client

User = get_user_model()


class ClientResource(resources.ModelResource):
    account_manager = fields.Field(
        column_name="account_manager",
        attribute="account_manager",
        widget=ForeignKeyWidget(User, "email"),
    )

    class Meta:
        model = Client
        skip_unchanged = True
        report_skipped = True
        fields = [
            "id",
            "client",
            "account_manager",
        ]
        import_id_fields = ["id"]

        export_order = [
            "client",
            "account_manager",
        ]


class ClientAdmin(ImportExportModelAdmin):
    show_full_result_count = False
    resource_class = ClientResource
    list_display = (
        "client",
        "id",
    )
    list_filter = (
        "client",
        "account_manager",
    )
    list_select_related = ("account_manager",)
    autocomplete_fields = ("account_manager",)
    search_fields = ("client", "account_manager__email")
    list_per_page = 25
    search_help_text = "Search by Client Name"
    ordering = ("client",)


admin.site.register(Client, ClientAdmin)
