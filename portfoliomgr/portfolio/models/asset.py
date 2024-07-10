from django.db import models
from djmoney.models.fields import CurrencyField

from .depot import Depot
from .security import Security


class Asset(models.Model):
    class Meta:
        unique_together = ["fk_security", "fk_depot"]

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
