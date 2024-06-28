from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bankaccounts/", views.BankAccountsList.as_view(), name="bankaccounts"),
    path("deposit/", views.deposit, name="deposit"),
]
