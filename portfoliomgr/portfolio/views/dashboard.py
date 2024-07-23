import logging

from django.db.models import Sum
from django.shortcuts import render

from ..market import get_market_price
from ..models.asset import Asset
from ..models.bank_account import BankAccount
from ..models.card import PaymentCard
from ..models.depot import Depot
from ..models.person import Person
from ..models.portfolio import Portfolio
from .utils.context import get_sidebar_context

logger = logging.getLogger(__name__)


def dashboard(request, id):
    context = {}
    context["sidebar"] = get_sidebar_context()
    person = Person.objects.filter(id=id)[0]
    context["person"] = person
    depots = Depot.objects.filter(fk_owner=person)
    accounts = BankAccount.objects.filter(fk_owner=person)
    cards = PaymentCard.objects.filter(fk_owner=person)
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

    context["depots"] = depots
    context["accounts"] = accounts
    context["cards"] = cards
    context["assets"] = assets

    return render(request, "portfolio/dashboard.html", context)
