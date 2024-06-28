from django import forms

from .models import AccountBooking


class DateInput(forms.DateInput):
    input_type = "date"
    format = "%d-%m-%Y"


class DepositForm(forms.ModelForm):
    class Meta:
        model = AccountBooking
        exclude = ["fk_transaction"]
        widgets = {
            "booking_date": DateInput(),
        }
