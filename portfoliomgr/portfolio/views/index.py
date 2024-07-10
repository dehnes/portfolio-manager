import logging

from django.db.models import Sum
from django.shortcuts import render

from ..market import get_market_price
from ..models.asset import Asset
from ..models.depot import Depot
from ..models.person import Person
from ..models.portfolio import Portfolio
from ..models.security import Security
from ..views.utils.context import get_sidebar_context

logger = logging.getLogger(__name__)


def index(request):
    context = {}
    context["sidebar"] = get_sidebar_context()

    logger.debug("This is a debug message")

    # Get all relevant data
    persons = Person.objects.all()
    securities = Security.objects.all()
    portfolios = Portfolio.objects.all()
    depots = Depot.objects.all()
    assets = Asset.objects.annotate(
        batch_positions_sum=(Sum("batch__batch_positions__quantity")),
    )
    # Calculating the Portfolio Values
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

    for sec in securities:
        sec.price = get_market_price(sec.ticker_symbol)

    context["persons"] = persons
    context["securities"] = securities
    return render(request, "portfolio/index.html", context)
