from datetime import date

from django.db import models

from .bank_account import BankAccount
from .transaction import Transaction


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
