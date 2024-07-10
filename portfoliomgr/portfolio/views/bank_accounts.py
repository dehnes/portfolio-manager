from django.views.generic.list import ListView

from ..models.bank_account import BankAccount


class BankAccountsList(ListView):
    # TODO add sidebarcontext
    model = BankAccount
