import logging
import pprint
from dataclasses import dataclass

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.list import ListView

from .forms import DepositForm, WithdrawForm
from .market import get_market_price
from .models import Asset, BankAccount, Depot, Person, Portfolio, Security, Transaction

logger = logging.getLogger(__name__)


def get_sidebar_context():
    return {"portfolios": Portfolio.objects.all()}


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


class Deposit(View):
    context = {}
    context["sidebar"] = get_sidebar_context()

    def get(self, request):
        self.context["form"] = DepositForm()
        return render(request, "portfolio/deposit.html", self.context)

    def form_valid(self, form):
        booking = form.save(commit=False)
        t = Transaction()
        t.description = form.cleaned_data("description")
        t.save()
        form.fk_transaction = t
        return super(Deposit, self).form_valid(form)

    def post(self, request):
        f = DepositForm(request.POST)
        if f.is_valid():
            self.form_valid(f)
            f.save()
        return render(request, "portfolio/deposit.html", context=self.context)


class Withdraw(View):
    context = {}
    context["sidebar"] = get_sidebar_context()

    def get(self, request):
        self.context["form"] = WithdrawForm()
        return render(request, "portfolio/withdraw.html", self.context)

    def post(self, request):

        return render(request, "portfolio/withdraw.html", self.context)


class BankAccountsList(ListView):
    model = BankAccount
