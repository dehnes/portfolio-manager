from datetime import date

from django.db import models

from .security import Security


# TODO Split into two models Dividend and DividendBooking?
class Dividend(models.Model):
    fk_security = models.ForeignKey(
        Security,
        related_name="Security",
        blank=False,
        on_delete=models.CASCADE,
        verbose_name="Security",
    )
    amount = models.DecimalField(
        max_digits=14, decimal_places=2, blank=False, verbose_name="Amount"
    )
    taxes = models.DecimalField(
        max_digits=14, decimal_places=2, blank=True, default=0.0, verbose_name="Taxes"
    )

    payment_date = models.DateField(default=date.today, verbose_name="Payment Date")

    def __str__(self) -> str:
        return (
            f"{self.fk_security} - Aomunt: {self.amount} - Date: {self.payment_date}€"
        )
