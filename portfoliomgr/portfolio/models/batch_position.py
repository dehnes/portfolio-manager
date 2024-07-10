from django.db import models
from djmoney.models.fields import MoneyField
from moneyed import Decimal

from .batch import Batch


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
    comment = models.CharField(max_length=100, blank=True)
