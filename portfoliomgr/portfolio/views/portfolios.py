import logging

from django.db.models import Sum
from django.shortcuts import render

from ..market import get_market_price
from ..models import Asset, Depot, Portfolio
from .utils.context import get_sidebar_context

logger = logging.getLogger(__name__)


def portfolios(request):
    context = {}
    context["sidebar"] = get_sidebar_context()

    assets = Asset.objects.annotate(
        batch_positions_sum=(Sum("batch__batch_positions__quantity")),
    )
    portfolios = Portfolio.objects.all()
    depots = Depot.objects.all()
    for asset in assets:
        if asset.batch_positions_sum > 0:
            asset.price = get_market_price(asset.fk_security.ticker_symbol)
            asset.balance = float(asset.price) * float(asset.batch_positions_sum)

    for depot in depots:
        depot.balance = 0.0
    for port in portfolios:
        port.balance = 0.0

    for depot in depots:
        for asset in assets:
            if asset.fk_depot == depot:
                depot.balance += asset.balance

    for port in portfolios:
        for depot in depots:
            if depot.fk_portfolio == port:
                port.balance += depot.balance

    context["portfolios"] = portfolios
    context["depots"] = depots
    context["assets"] = assets

    return render(request, "portfolio/portfolios.html", context)
