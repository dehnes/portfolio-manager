from datetime import date

from django.db import models

from .batch_position import BatchPosition
from .transaction import Transaction


class BatchPositionBooking(models.Model):
    fk_batch_position = models.ForeignKey(
        BatchPosition,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name="Batch Position",
    )
    fk_transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, blank=False, verbose_name="Transaction"
    )
    quantity = models.DecimalField(
        max_digits=14, decimal_places=2, blank=False, verbose_name="Quantity"
    )
    booking_date = models.DateField(
        default=date.today, blank=False, verbose_name="Booking Date"
    )
    description = models.TextField(
        max_length=500, blank=True, verbose_name="Description"
    )
