from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
from djmoney.forms import MoneyField
from moneyed import Decimal

from ..models.bank_account import BankAccount
from ..models.depot import Depot
from ..models.security import Security


class DateInput(forms.DateInput):
    input_type = "date"
    format = "%d-%m-%Y"


class BuyForm(forms.Form):
    security = forms.ModelChoiceField(queryset=Security.objects.all(), label="Security")
    bank_account = forms.ModelChoiceField(
        queryset=BankAccount.objects.all(), label="Bank Account"
    )
    depot = forms.ModelChoiceField(queryset=Depot.objects.all(), label="Depot")
    buy_date = forms.DateField(widget=DateInput(), localize=True)
    description = forms.CharField(
        label="Description",
        max_length=500,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Provide a menaingful description of the overall pruchase"
            }
        ),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("security", css_class="col-md-4 mb-0"),
                Column("bank_account", css_class="col-md-4 mb-0"),
                Column("depot", css_class="col-md-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("description", css_class="col-md-8 mb-0"),
                Column("buy_date", css_class="col-md-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("quantity_1", css_class="col-md-2 mb-0"),
                Column("price_1", css_class="col-md-2 mb-0"),
                Column("buy_fee_1", css_class="col-md-2 mb-0"),
                Column("yeearly_fee_1", css_class="col-md-2 mb-0"),
                Column("comment_1", css_class="col-md-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("quantity_2", css_class="col-md-2 mb-0"),
                Column("price_2", css_class="col-md-2 mb-0"),
                Column("buy_fee_2", css_class="col-md-2 mb-0"),
                Column("yeearly_fee_2", css_class="col-md-2 mb-0"),
                Column("comment_2", css_class="col-md-4 mb-0"),
                css_class="form-row",
            ),
            Submit("submit", "Buy", css_class="btn btn-primary"),
        )
