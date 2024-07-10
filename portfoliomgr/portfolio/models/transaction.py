import uuid

from django.db import models

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

    def __str__(self):
        return f"{self.transaction_type} - {self.date} - Status: {self.status}"
