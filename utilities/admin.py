from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Supplier, Utility


class SupplierResource(resources.ModelResource):
    class Meta:
        model = Supplier
        skip_unchanged = True
        report_skipped = True
        # fields = ["supplier"]
        import_id_fields = ["supplier"]


class SupplierAdmin(ImportExportModelAdmin):
    resource_class = SupplierResource
    list_display = (
        "supplier",
        "meter_email",
    )
    list_filter = ("supplier",)
    ordering = ("supplier",)
    search_fields = ("supplier",)


admin.site.register(Supplier, SupplierAdmin)


class UtilityResource(resources.ModelResource):
    class Meta:
        model = Utility
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ["utility"]


class UtilityAdmin(admin.ModelAdmin):
    list_display = ("utility",)
    search_fields = ("utility",)
    ordering = ("utility",)


admin.site.register(Utility, UtilityAdmin)
