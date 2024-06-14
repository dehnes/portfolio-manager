import uuid
from abc import abstractmethod

from django.db import models
from djmoney.models.fields import CurrencyField, MoneyField

# Open TODOs:
# TODO add Dividend Payments to Model
# TODO add buy, sell, deposit, withdraw methods to Model


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=100, blank=False)
    surname = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f"{self.surname} {self.name}"


class Institute(models.Model):
    bic = models.CharField(max_length=8, blank=False, unique=True)
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    name = models.CharField(max_length=100, blank=False)
    fk_owner = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


ACT = "ACTIVE"
SUS = "SUSPENDED"
DEACT = "DEACTIVATED"

ACCOUNT_STATUS_CHOICES = ((ACT, "Active"), (SUS, "Suspended"), (DEACT, "Deactivated"))


class BankAccount(models.Model):
    iban = models.CharField(unique=True, max_length=22)
    name = models.CharField(max_length=100, default="tbd")
    institue = models.ForeignKey(Institute, on_delete=models.CASCADE)
    balance = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="EUR",
        default=0,
    )
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    account_status = models.CharField(
        max_length=15, choices=ACCOUNT_STATUS_CHOICES, default="ACTIVE"
    )


DEPOSIT = "DEPOSIT"
WITHDRAWAL = "WITHDRAWAL"
TRANSFER = "TRANSFER"

TRANSACTION_TYPE_CHOICES = (
    (DEPOSIT, "Deposit"),
    (WITHDRAWAL, "Withdrawal"),
    (TRANSFER, "Transfer"),
)


class Transaction(models.Model):
    models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fk_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    amount = MoneyField(
        max_digits=14, decimal_places=2, default_currency="EUR", default=0
    )
    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=100, blank=True)
    transaction_type = models.CharField(
        max_length=15, choices=TRANSACTION_TYPE_CHOICES, default="DEPOSIT"
    )

    def save(self, *args, **kwargs):
        self.fk_account.balance += self.amount
        self.fk_account.save()
        super(Transaction, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.fk_account.balance -= self.Amount
        self.fk_account.save()
        super(Transaction, self).delete(*args, **kwargs)


class Depot(models.Model):
    name = models.CharField(max_length=100, blank=False)
    fk_institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    fk_portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Security(models.Model):
    name = models.CharField(max_length=100, blank=False)

    @abstractmethod
    def get_actual_price(self) -> float: ...


class Stock(Security):
    wkn = models.CharField(max_length=15)
    isin = models.CharField(max_length=25)

    def get_actual_price(self) -> float:
        pass
        # TODO Implement get_actual_price in Model: Stock


class ETF(Security):
    wkn = models.CharField(max_length=15)
    isin = models.CharField(max_length=25)

    def get_actual_price(self) -> float:
        pass
        # TODO Implement get_actual_price in Model: ETF


class Asset(models.Model):
    security = models.ForeignKey(Security, on_delete=models.CASCADE, blank=False)
    base_currency = CurrencyField(default="EUR", blank=False)


class Batch(models.Model):
    in_date = models.DateField(blank=False)
    fk_asset = models.ForeignKey(Asset, on_delete=models.CASCADE, blank=False)


class BatchPosition(models.Model):
    quantity = models.DecimalField(max_digits=14, decimal_places=2, blank=False)
    buyPrice = MoneyField(
        blank=False, max_digits=14, decimal_places=2, default_currency="EUR"
    )
    fk_batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
