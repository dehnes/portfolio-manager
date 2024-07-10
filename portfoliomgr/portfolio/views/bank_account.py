import logging

from django.shortcuts import render

from ..models import AccountBooking, BankAccount
from .utils.context import get_sidebar_context

logger = logging.getLogger(__name__)


def bankaccount(request, id):
    context = {}
    context["sidebar"] = get_sidebar_context()
    account = BankAccount.objects.filter(id=id)[0]
    bookings = AccountBooking.objects.filter(fk_bank_account=account)
    balance = 0.0
    for booking in bookings:
        balance += float(booking.value)
    context["account"] = account
    context["bookings"] = bookings
    context["balance"] = balance
    return render(
        request,
        "portfolio/bankaccount.html",
        context,
    )
