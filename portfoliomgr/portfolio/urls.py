from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bankaccounts/", views.BankAccountsList.as_view(), name="bankaccounts"),
    path("portfolios/", views.portfolios, name="portfolios"),
    path("deposit/", views.Deposit.as_view(), name="deposit"),
]
