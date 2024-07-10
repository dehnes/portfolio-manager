import logging

from django.shortcuts import render

from ..forms.withdraw import WithdrawForm
from ..market import get_market_price
from ..models.transaction import WITHDRAWAL, Transaction
from .utils.context import get_sidebar_context

logger = logging.getLogger(__name__)


def withdraw(request):
    context = {}
    context["sidebar"] = get_sidebar_context()
    if request.method == "POST":
        form = WithdrawForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.fk_transaction = Transaction.objects.create()
            form.instance.fk_transaction.description = form.cleaned_data["description"]
            form.instance.fk_transaction.transaction_type = WITHDRAWAL
            form.instance.value = float(form.cleaned_data["value"]) * (-1)
            form.instance.fk_transaction.save()
            form.save()
            context["fund", "w"]
            return render(request, "portfolio/funding_success.html", context)

        else:
            logger.error("Error: WithdrawForm is not valid!")
    else:
        context["form"] = WithdrawForm()

    return render(request, "portfolio/withdraw.html", context)
