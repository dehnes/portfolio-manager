from django.db import models
from djmoney.models.fields import MoneyField

from .institute import Institute
from .person import Person

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
