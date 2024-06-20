# Register your models here.
from django.contrib import admin

from .models import (
    Asset,
    BankAccount,
    Batch,
    BatchPosition,
    Depot,
    Institute,
    Person,
    Portfolio,
    Security,
)


class PersonAdmin(admin.ModelAdmin):
    pass


class InstituteAdmin(admin.ModelAdmin):
    list_display = (
        "bic",
        "name",
        "short_name",
    )


class BankAccountAdmin(admin.ModelAdmin):
    list_display = (
        "iban",
        "name",
        "fk_institute",
        "fk_owner",
        "account_status",
        "account_type",
    )


class PortfolioAdmin(admin.ModelAdmin):
    pass


class DepotAdmin(admin.ModelAdmin):
    pass


class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "fk_security",
        "fk_depot",
    )


class BatchAdmin(admin.ModelAdmin):
    list_display = (
        "in_date",
        "fk_asset",
    )


class BatchPositionAdmin(admin.ModelAdmin):
    list_display = (
        "fk_batch",
        "quantity",
        "buy_price",
        "buy_fee",
        "sell_fee",
        "yearly_fee",
    )


class SecurityAdmin(admin.ModelAdmin):
    list_display = (
        "wkn",
        "isin",
        "name",
        "ticker_symbol",
    )


admin.site.register(Person, PersonAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Depot, DepotAdmin)
admin.site.register(Institute, InstituteAdmin)
admin.site.register(BankAccount, BankAccountAdmin)

admin.site.register(Asset, AssetAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(BatchPosition, BatchPositionAdmin)
admin.site.register(Security, SecurityAdmin)
