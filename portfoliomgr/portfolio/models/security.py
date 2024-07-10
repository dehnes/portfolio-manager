from django.db import models

from ..market import get_market_price


class Security(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name="Name")
    wkn = models.CharField(max_length=15, unique=True, verbose_name="WKN")
    isin = models.CharField(max_length=25, unique=True, verbose_name="ISIN")
    ticker_symbol = models.CharField(
        max_length=5,
        verbose_name="Ticker Symbol",
        default="",
    )

    def get_actual_price(self) -> float:
        return get_market_price(self.ticker_symbol)

    actual_price = property(get_actual_price)

    def __str__(self):
        return self.name
