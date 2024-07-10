from django.db import models

from .asset import Asset


class Batch(models.Model):
    in_date = models.DateField(blank=False, verbose_name="Date of inflow")
    fk_asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, blank=False, verbose_name="Asset"
    )
    description = models.CharField(max_length=500, default="", blank=True)

    def __str__(self) -> str:
        return f"{self.fk_asset} Bought: {self.in_date}"
