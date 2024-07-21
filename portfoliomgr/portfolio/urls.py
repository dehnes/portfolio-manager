from django.urls import path

from . import views
from .views.asset import asset
from .views.bank_account import bankaccount
from .views.bank_accounts import BankAccountsList
from .views.buy import buy
from .views.dashboard import dashboard
from .views.deposit import deposit
from .views.index import index
from .views.portfolio import portfolio
from .views.portfolios import portfolios
from .views.withdraw import withdraw

urlpatterns = [
    path("", index, name="index"),
    path("assets/<int:id>", asset, name="asset"),
    path("bankaccounts/", BankAccountsList.as_view(), name="bankaccounts"),
    path("bankaccount/<int:id>", bankaccount, name="bankaccount"),
    path("buy/", buy, name="buy"),
    path("dashboards/<int:id>", dashboard, name="dashboard"),
    path("deposit/", deposit, name="deposit"),
    path("portfolios/", portfolios, name="portfolios"),
    path("portfolios/<int:id>", portfolio, name="portfolio"),
    path("withdraw/", withdraw, name="withdraw"),
]
