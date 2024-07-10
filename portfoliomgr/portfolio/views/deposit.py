import logging

from django.shortcuts import render

from ..forms.deposit import DepositForm
from ..models import Transaction
from .utils.context import get_sidebar_context

logger = logging.getLogger(__name__)


def deposit(request):
    context = {}
    context["sidebar"] = get_sidebar_context()
    if request.method == "POST":
        form = DepositForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.fk_transaction = Transaction.objects.create()
            form.instance.fk_transaction.description = form.cleaned_data["description"]
            form.instance.fk_transaction.save()
            form.save()
            context["fund", "d"]
            return render(request, "portfolio/funding_success.html", context)
        else:
            logger.error("Error: DepositForm is not valid!")
    else:
        context["form"] = DepositForm()
    return render(request, "portfolio/deposit.html", context)
