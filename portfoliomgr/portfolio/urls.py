from django.urls import path

from . import views
from .views import index

urlpatterns = [
    path("", index, name="index"),
    path("bankaccounts/", views.BankAccountsList.as_view(), name="bankaccounts"),
    path("portfolios/", views.portfolios, name="portfolios"),
    path("portfolios/<int:id>", views.portfolio, name="portfolio"),
    path("deposit/", views.Deposit.as_view(), name="deposit"),
]
