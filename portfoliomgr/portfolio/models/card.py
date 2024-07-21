# status bool
# type Credit, Debit, EC,
# Payment Service: Visa, Master
# logo
# owner
# ref account
# cvc blank =true
# valid until
# emergency phone

# Filialnummer
# Kartenfolgenummer
# Kartenprüfnummer

# https://pypi.org/project/django-credit-cards/

# TODO implement credit card model class
# TODO dedicated giro card model?

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_resized import ResizedImageField

from ..models.bank_account import BankAccount
from ..models.person import Person


class PaymentProvider(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name="Name")
    short_name = models.CharField(max_length=10, default="", verbose_name="Short Name")
    logo = ResizedImageField(size=[300, 300], upload_to="logos", force_format="PNG")

    def __str__(self) -> str:
        return self.name


CREDIT = "Credit"
DEBIT = "Debit"
EC = "EC"
OTHER = "Other"

PAYMENT_TYPE_CHOICES = (
    (CREDIT, "Credit"),
    (DEBIT, "Debit"),
    (EC, "Electronic Cash"),
    (OTHER, "Other"),
)

# TODO add verbose names


class PaymentCard(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name="Name")
    type = models.CharField(
        max_length=20, choices=PAYMENT_TYPE_CHOICES, verbose_name="Type"
    )
    fk_payment_service = models.ForeignKey(
        PaymentProvider,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Payment Service",
    )
    fk_owner = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="Owner")
    fk_account = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, verbose_name="Bank Account"
    )
    card_number = models.CharField(max_length=24, verbose_name="Card Number")
    valid_month = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name="MM",
    )
    valid_year = models.IntegerField(
        default=2022, validators=[MinValueValidator(2022)], verbose_name="YY"
    )
    cvc = models.CharField(max_length=3, blank=True, verbose_name="CVC")
    karten_folge_nummer = models.IntegerField(
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        verbose_name="Kartenfolgenummer",
    )
    status = models.BooleanField(default=True, verbose_name="Active")

    def __str__(self) -> str:
        return self.name
