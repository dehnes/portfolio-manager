import logging
import pprint
from dataclasses import dataclass

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.views.generic import View
from django.views.generic.list import ListView

from .forms import DepositForm, WithdrawForm
from .market import get_market_price
from .models import (
    DEPOSIT,
    WITHDRAWAL,
    AccountBooking,
    Asset,
    BankAccount,
    Depot,
    Person,
    Portfolio,
    Security,
    Transaction,
)

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


def deposit(request):
    if request.method == "POST":
        form = DepositForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.fk_transaction = Transaction.objects.create()
            form.instance.fk_transaction.description = form.cleaned_data["description"]
            form.instance.fk_transaction.save()
            form.save()
            return render(request, "portfolio/funding_success.html", {"fund": "d"})
        else:
            logger.error("Error: DepositForm is not valid!")
    else:
        form = DepositForm()
    return render(request, "portfolio/deposit.html", {"form": form})


def withdraw(request):
    if request.method == "POST":
        form = WithdrawForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.fk_transaction = Transaction.objects.create()
            form.instance.fk_transaction.description = form.cleaned_data["description"]
            form.instance.fk_transaction.transaction_type = WITHDRAWAL
            form.instance.value = float(form.cleaned_data["value"]) * (-1)
            form.instance.fk_transaction.save()
            form.save()
            return render(request, "portfolio/funding_success.html", {"fund": "w"})

        else:
            logger.error("Error: WithdrawForm is not valid!")
    else:
        form = WithdrawForm()

    return render(request, "portfolio/withdraw.html", {"form": form})


class BankAccountsList(ListView):
    model = BankAccount


def bankaccount(request, id):
    account = BankAccount.objects.filter(id=id)[0]
    bookings = AccountBooking.objects.filter(fk_bank_account=account)
    balance = 0.0
    for booking in bookings:
        balance += float(booking.value)
    return render(
        request,
        "portfolio/bankaccount.html",
        {"account": account, "bookings": bookings, "balance": balance},
    )
