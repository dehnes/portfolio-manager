# Register your models here.
from django.contrib import admin
from django.utils.html import format_html

from .models.account_booking import AccountBooking
from .models.asset import Asset
from .models.bank_account import BankAccount
from .models.batch import Batch
from .models.batch_position import BatchPosition
from .models.batch_position_booking import BatchPositionBooking
from .models.card import PaymentCard, PaymentProvider
from .models.depot import Depot
from .models.institute import Institute
from .models.person import Person
from .models.portfolio import Portfolio
from .models.security import Security
from .models.transaction import Transaction


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "name" ,
        "surname",
        "picture",
    )


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
        "description",
    )


class BatchPositionAdmin(admin.ModelAdmin):
    list_display = (
        "fk_batch",
        "quantity",
        "buy_price",
        "buy_fee",
        "sell_fee",
        "yearly_fee",
        "comment",
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


class BatchPositionBookingAdmin(admin.ModelAdmin):
    list_display = (
        "fk_batch_position",
        "fk_transaction",
        "quantity",
        "description",
        "booking_date",
    )


class PaymentProviderAdmin(admin.ModelAdmin):

    def image_tag(self, obj):  # sourcery skip: use-fstring-for-formatting
        return format_html(
            '<img src="{}" style="max-width:48px; max-height:48px"/>'.format(
                obj.logo.url
            )
        )

    list_display = (
        "image_tag",
        "name",
        "short_name",
    )


class PaymentCardAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
        "fk_payment_service",
        "fk_owner",
        "fk_account",
        "card_number",
        "valid_month",
        "valid_year",
        "cvc",
        "karten_folge_nummer",
        "status",
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
admin.site.register(BatchPositionBooking, BatchPositionBookingAdmin)
admin.site.register(PaymentProvider, PaymentProviderAdmin)
admin.site.register(PaymentCard, PaymentCardAdmin)
