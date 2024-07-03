import pprint
from dataclasses import dataclass
from typing import Any

from django.contrib import messages
from django.db.models import Avg, CharField, F, FloatField, IntegerField, Min, Sum
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.list import ListView

from .forms import DepositForm
from .market import get_market_price
from .models import (
    AccountBooking,
    Asset,
    BankAccount,
    Depot,
    Person,
    Portfolio,
    Security,
    Transaction,
)


def index(request):
    context = {}

    persons = Person.objects.all()
    securities = Security.objects.all()
    for sec in securities:
        sec.price = get_market_price(sec.ticker_symbol)

    context["persons"] = persons
    context["securities"] = securities
    return render(request, "portfolio/index.html", context)


def portfolios(request):
    context = {}

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
        form = DepositForm(request.POST)
        if form.is_valid():

            account = form.cleaned_data["fk_bank_account"]
            value = form.cleaned_data["value"]
            bdate = form.cleaned_data["booking_date"]

            print(f"Bank: {account}")
            print(f"Value: {value}")
            print(f"Booking Date: {bdate}")
            # BankAccount.objects.get(name=account).update(balance=F("balance") + value)
            # BankAccount.objects.filter(account=account).update(
            #    balance=F("balance") + value
            # )
            # return render(request, "portfolio/deposit_success.html", {"amount": amount})
    else:
        form = DepositForm()
    return render(
        request,
        "portfolio/deposit.html",
    )


class Deposit(View):
    context = {}

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
        return render(request, "portfolio/deposit.html", {})


class BankAccountsList(ListView):
    model = BankAccount
