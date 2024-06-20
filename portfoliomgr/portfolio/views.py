import pprint

import yfinance as yf
from django.db.models import Avg, Sum
from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Asset, BankAccount, Depot, Portfolio


def index(request):
    context = {}

    assets = Asset.objects.annotate(
        batch_positions_sum=(Sum("batch__batch_positions__quantity"))
    )

    context["portfolios"] = Portfolio.objects.all()
    context["depots"] = Depot.objects.all()
    context["assets"] = assets
    return render(request, "portfolio/index.html", context)


class BankAccountsList(ListView):
    model = BankAccount
