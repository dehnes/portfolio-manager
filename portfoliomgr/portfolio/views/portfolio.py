import logging

from django.db.models import Sum
from django.shortcuts import render

from ..market import get_market_price
from ..models import Asset, Depot, Portfolio
from .utils.context import get_sidebar_context

logger = logging.getLogger(__name__)


def portfolio(request, id):
    context = {}
    context["sidebar"] = get_sidebar_context()
    port = Portfolio.objects.filter(id=id)[0]
    depots = Depot.objects.filter(fk_portfolio=port)
    assets = Asset.objects.annotate(
        batch_positions_sum=(Sum("batch__batch_positions__quantity")),
    )
    for asset in assets:
        if asset.batch_positions_sum > 0:
            asset.price = get_market_price(asset.fk_security.ticker_symbol)
            asset.balance = float(asset.price) * float(asset.batch_positions_sum)
    for depot in depots:
        depot.balance = 0.0
    for depot in depots:
        for asset in assets:
            if asset.fk_depot == depot:
                depot.balance += asset.balance

    context["port"] = port
    context["depots"] = depots
    context["assets"] = assets

    return render(request, "portfolio/portfolio.html", context)
