from django import forms
from .models import Will


class DateInput(forms.DateInput):

    input_type = 'date'
    # date_field=forms.DateField(widget=DateInput)


class WillForm(forms.ModelForm):
    """WillForm definition."""
    date_of_execution = forms.DateField(widget=DateInput)
    date_deposited = forms.DateField(widget=DateInput)

    class Meta:
        model = Will
        exclude = ('user',)

    # TODO: Define form fields here
