from django import forms
from djmoney.forms import MoneyField
from moneyed import Decimal

from .models import AccountBooking, BankAccount, Depot, Security, Transaction


class DateInput(forms.DateInput):
    input_type = "date"
    format = "%d-%m-%Y"


class DepositForm(forms.ModelForm):
    class Meta:
        model = AccountBooking
        fields = "__all__"
        exclude = ("fk_transaction",)
        localized_fields = ["booking_date"]
        widgets = {"booking_date": DateInput()}


class WithdrawForm(forms.ModelForm):
    class Meta:
        model = AccountBooking
        fields = "__all__"
        exclude = ("fk_transaction",)
        localized_fields = ["booking_date"]
        widgets = {"booking_date": DateInput()}


class BuyStockForm(forms.Form):
    security = forms.ChoiceField(label="Security")
    quantity_1 = forms.IntegerField()
    price_2 = forms.DecimalField(max_digits=10, decimal_places=2)
    quantity_1 = forms.IntegerField()
    price_2 = forms.DecimalField(max_digits=10, decimal_places=2)
    fee = forms.DecimalField(max_digits=10, decimal_places=2)


class BuyForm(forms.Form):
    security = forms.ModelChoiceField(queryset=Security.objects.all(), label="Security")
    bank_account = forms.ModelChoiceField(
        queryset=BankAccount.objects.all(), label="Bank Account"
    )
    depot = forms.ModelChoiceField(queryset=Depot.objects.all(), label="Depot")
    buy_date = forms.DateField(widget=DateInput(), localize=True)
    description = forms.CharField(
        label="Description", max_length=500, widget=forms.Textarea()
    )

    # BATCH POSITION 1
    quantity_1 = forms.DecimalField(max_digits=14, decimal_places=2, label="Quantity 1")
    price_1 = MoneyField(
        max_digits=14,
        min_value=0,
        default_amount=Decimal("0.0"),
        default_currency="EUR",
        label="Price 1",
    )
    buy_fee_1 = MoneyField(
        max_digits=14,
        min_value=0,
        default_amount=Decimal("0.0"),
        default_currency="EUR",
        label="Buy Fee",
    )
    yearly_fee_1 = MoneyField(
        max_digits=14,
        min_value=0,
        default_amount=Decimal("0.0"),
        default_currency="EUR",
        label="Yearly Fee",
    )
    comment_1 = forms.CharField(max_length=100, required=False)
    # BATCH POSITION 2
    quantity_2 = forms.DecimalField(
        max_digits=14, decimal_places=2, label="Quantity 2", required=False
    )
    price_2 = MoneyField(
        max_digits=14,
        min_value=0,
        default_amount=Decimal("0.0"),
        default_currency="EUR",
        label="Price 2",
        required=False,
    )
    buy_fee_2 = MoneyField(
        max_digits=14,
        min_value=0,
        default_amount=Decimal("0.0"),
        default_currency="EUR",
        label="Buy Fee 2",
        required=False,
    )
    yearly_fee_2 = MoneyField(
        max_digits=14,
        min_value=0,
        default_amount=Decimal("0.0"),
        default_currency="EUR",
        label="Yearly Fee 2",
        required=False,
    )
    comment_2 = forms.CharField(max_length=100, required=False)
