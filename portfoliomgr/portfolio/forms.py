from django import forms

from .models import AccountBooking, Transaction


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
