from django.views.generic.list import ListView

from ..models import BankAccount


class BankAccountsList(ListView):
    # TODO add sidebarcontext
    model = BankAccount
