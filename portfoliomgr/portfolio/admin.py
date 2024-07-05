# Register your models here.
from django.contrib import admin

from .models import (
    AccountBooking,
    Asset,
    BankAccount,
    Batch,
    BatchPosition,
    Depot,
    Institute,
    Person,
    Portfolio,
    Security,
    Transaction,
)


class PersonAdmin(admin.ModelAdmin):
    pass


class InstituteAdmin(admin.ModelAdmin):
    list_display = (
        "bic",
        "name",
        "short_name",
        "logo",
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
    list_display = (
        "name",
        "fk_institute",
        "fk_portfolio",
        "fk_owner",
        "is_active",
    )


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


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "description",
        "transaction_type",
        "status",
    )


class AccountBookingAdmin(admin.ModelAdmin):
    list_display = (
        "fk_bank_account",
        "fk_transaction",
        "value",
        "description",
        "booking_date",
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
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(AccountBooking, AccountBookingAdmin)
