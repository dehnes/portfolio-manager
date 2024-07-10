from django import forms

from ..models.account_booking import AccountBooking


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
