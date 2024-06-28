from dataclasses import dataclass
from datetime import date
from typing import List


def annualize(start_date: date, end_date: date = date.today(), value: float = 0.0):
    if start_date > end_date:
        raise ValueError("Start date must not be larger than end date")
    return value / (end_date - start_date).days * 365


@dataclass
class KPISet:
    capital_invested: float = 0.0
    current_price: float = 1.0
    dividend: float = 0.0
    tax: float = 0.0
    cost: float = 0.0
    buy_date: date = date.today
    end_date: date = date.today

    @property
    def profit(self):
        return self.current_price + self.dividend - self.capital_invested

    @property
    def net_profit(self) -> float:
        return self.net_profit - self.tax - self.cost

    @property
    def net_return(self) -> float:
        # gewinn + dividende - kosten - steuern / eingesetztes Kapital
        return self.net_profit / self.capital_invested

    @property
    def net_return_annualized(self) -> float:
        return annualize(self.buy_date, self.end_date, self.net_return)


def get_weighted_net_return_annualized(items: List[KPISet]) -> float:
    for item in item:
        pass  # TODO implement


# über mehrere Batches
# 1. alle renditen ausrechnen
# 2. renditen gewichten (nach eingesetztem Kapital)
