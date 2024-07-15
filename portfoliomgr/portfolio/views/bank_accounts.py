from django.views.generic.list import ListView

from ..models.bank_account import BankAccount
from .utils.context import get_sidebar_context


class BankAccountsList(ListView):
    model = BankAccount

    def get_context_data(self, **kwargs):
        context = super(BankAccountsList, self).get_context_data(**kwargs)
        context["sidebar"] = get_sidebar_context()
        return context
