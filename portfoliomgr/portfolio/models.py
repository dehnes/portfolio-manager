import uuid
from abc import abstractmethod
from datetime import date

from django.db import models
from django_resized import ResizedImageField
from djmoney.models.fields import CurrencyField, MoneyField

from .market import get_market_price

# Open TODOs:
# TODO add Dividend Payments to Model
# TODO add buy, sell, deposit, withdraw methods to Model


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name="Name")
    surname = models.CharField(max_length=100, blank=False, verbose_name="Surname")
    picture = ResizedImageField(
        size=[500, 500], upload_to="profile_pics", force_format="PNG"
    )

    def __str__(self):
        return f"{self.surname} {self.name}"


class Institute(models.Model):
    bic = models.CharField(max_length=12, blank=False, unique=True, verbose_name="BIC")
    name = models.CharField(max_length=100, blank=False, verbose_name="Name")
    short_name = models.CharField(
        max_length=20, default="", blank=True, verbose_name="Short Name"
    )
    logo = ResizedImageField(size=[300, 300], upload_to="logos", force_format="PNG")

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name="Name")
    fk_owner = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Owner")

    def __str__(self):
        return self.name


ACT = "ACTIVE"
SUS = "SUSPENDED"
DEACT = "DEACTIVATED"

ACCOUNT_STATUS_CHOICES = ((ACT, "Active"), (SUS, "Suspended"), (DEACT, "Deactivated"))

GIRO = "GIRO"
TAGESGELD = "TAGESGELD"

ACCOUNT_TYPE_CHOICES = (
    (GIRO, "Giro"),
    (TAGESGELD, "Tagesgeld"),
)


class BankAccount(models.Model):
    iban = models.CharField(unique=True, max_length=22, verbose_name="IBAN")
    name = models.CharField(max_length=100, default="tbd", verbose_name="Name")
    fk_institute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, verbose_name="Institute", default=0
    )
    balance = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="EUR",
        default=0,
        verbose_name="Balance",
    )
    fk_owner = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name="Owner", default=0
    )
    account_status = models.CharField(
        max_length=15,
        choices=ACCOUNT_STATUS_CHOICES,
        default="ACTIVE",
        verbose_name="Account Status",
    )
    account_type = models.CharField(
        max_length=15,
        choices=ACCOUNT_TYPE_CHOICES,
        default="GIRO",
        verbose_name="Account Type",
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.fk_institute.short_name})"


DEPOSIT = "DEPOSIT"
WITHDRAWAL = "WITHDRAWAL"
TRANSFER = "TRANSFER"
SELL = "SELL"
BUY = "BUY"

TRANSACTION_TYPE_CHOICES = (
    (DEPOSIT, "Deposit"),
    (WITHDRAWAL, "Withdrawal"),
    (TRANSFER, "Transfer"),
    (SELL, "Sell"),
    (BUY, "Buy"),
)
DRAFT = "DRAFT"
EXECUTED = "EXECUTED"
FAILED = "FAILED"
ROLLED_BACK = "ROLLED_BACK"

TR_STATUS_CHOICES = (
    (DRAFT, "Draft"),
    (EXECUTED, "Executed"),
    (FAILED, "Failed"),
    (ROLLED_BACK, "Rolled back"),
)


class Transaction(models.Model):
    models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="UUID"
    )

    date = models.DateField(auto_now_add=True, verbose_name="Date")
    description = models.TextField(
        max_length=500, blank=True, verbose_name="Description"
    )
    transaction_type = models.CharField(
        max_length=15,
        choices=TRANSACTION_TYPE_CHOICES,
        default="DEPOSIT",
    )
    status = models.CharField(max_length=11, choices=TR_STATUS_CHOICES, default=DRAFT)


class AccountBooking(models.Model):
    fk_bank_account = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, blank=False, verbose_name="Bank Account"
    )
    fk_transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, blank=False
    )
    value = models.DecimalField(
        max_digits=14, decimal_places=2, blank=False, verbose_name="Value"
    )
    booking_date = models.DateField(
        default=date.today, blank=False, verbose_name="Booking Date"
    )
    description = models.TextField(
        max_length=500, blank=True, verbose_name="Description"
    )


class Depot(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name="Name")
    fk_institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        verbose_name="Institute",
    )
    fk_portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, verbose_name="Portfolio"
    )
    fk_owner = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Owner")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    def __str__(self):
        return f"{self.name} ({self.fk_owner.surname} - {self.fk_institute.short_name})"


class Security(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name="Name")
    wkn = models.CharField(max_length=15, unique=True, verbose_name="WKN")
    isin = models.CharField(max_length=25, unique=True, verbose_name="ISIN")
    ticker_symbol = models.CharField(
        max_length=5,
        verbose_name="Ticker Symbol",
        default="",
    )

    def get_actual_price(self) -> float:
        return get_market_price(self.ticker_symbol)

    actual_price = property(get_actual_price)

    def __str__(self):
        return self.name


class Asset(models.Model):
    fk_security = models.ForeignKey(
        Security,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name="Security",
        default=0,
        related_name="security",
    )
    fk_depot = models.ForeignKey(
        Depot, on_delete=models.CASCADE, blank=False, verbose_name="Depot"
    )
    base_currency = CurrencyField(
        default="EUR", blank=False, verbose_name="Base Currency"
    )

    def __str__(self) -> str:
        return f"{self.fk_security} ({self.fk_depot})"


class Batch(models.Model):
    in_date = models.DateField(blank=False, verbose_name="Date of inflow")
    fk_asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, blank=False, verbose_name="Asset"
    )

    def __str__(self) -> str:
        return f"{self.fk_asset} Bought: {self.in_date}"


from moneyed import Decimal


class BatchPosition(models.Model):
    quantity = models.DecimalField(
        max_digits=14, decimal_places=2, blank=False, default=0, verbose_name="Quantity"
    )
    buy_price = MoneyField(
        blank=True,
        max_digits=14,
        decimal_places=2,
        default_currency="EUR",
        verbose_name="Buy Price",
        default=Decimal("0.0"),
    )
    buy_fee = MoneyField(
        blank=True,
        max_digits=14,
        decimal_places=2,
        default_currency="EUR",
        verbose_name="Buy Fee",
        default=Decimal("0.0"),
    )
    sell_fee = MoneyField(
        blank=True,
        max_digits=14,
        decimal_places=2,
        default_currency="EUR",
        verbose_name="Sell Fee",
        default=Decimal("0.0"),
    )
    yearly_fee = MoneyField(
        blank=True,
        max_digits=14,
        decimal_places=2,
        default_currency="EUR",
        verbose_name="Yearly Fee",
        default=Decimal("0.0"),
    )
    fk_batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        verbose_name="Batch",
        blank=False,
        related_name="batch_positions",
    )


class DividendPayment(models.Model):
    count = models.DecimalField(max_digits=14, decimal_places=2, blank=False)
    value_each = models.DecimalField(max_digits=14, decimal_places=2, blank=False)
    taxes = models.DecimalField(max_digits=14, decimal_places=2, blank=False)
    fk_asset = models.ForeignKey(Asset, on_delete=models.CASCADE, blank=False)
    payment_date = models.DateField(default=date.today)

    @property
    def gross_value(self):
        return float(self.count) * float(self.value_each)

    @property
    def net_value(self):
        return self.gross_amount() - self.taxes

    def __str__(self) -> str:
        return f"{self.fk_asset} - Quantity: {self.count} - Total: {self.value_each}€"
