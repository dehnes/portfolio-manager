from django import forms

from .models import AccountBooking


class DateInput(forms.DateInput):
    input_type = "date"
    format = "%d-%m-%Y"


class DepositForm(forms.ModelForm):
    class Meta:
        model = AccountBooking
        fields = [
            "fk_bank_account",
            "fk_transaction",
            "value",
            "booking_date",
            "description",
        ]
        widgets = {"booking_date": DateInput(), "fk_transaction": forms.HiddenInput()}
