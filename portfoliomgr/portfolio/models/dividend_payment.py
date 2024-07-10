from datetime import date

from django.db import models

from .asset import Asset


# TODO Split into two models Dividend and DividendBooking?
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
