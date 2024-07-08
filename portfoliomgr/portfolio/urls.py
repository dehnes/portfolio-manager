from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bankaccounts/", views.BankAccountsList.as_view(), name="bankaccounts"),
    path("bankaccount/<int:id>", views.bankaccount, name="bankaccount"),
    path("portfolios/", views.portfolios, name="portfolios"),
    path("portfolios/<int:id>", views.portfolio, name="portfolio"),
    path("deposit/", views.deposit, name="deposit"),
    path("withdraw/", views.withdraw, name="withdraw"),
    path("buy/", views.buy, name="buy"),
]
