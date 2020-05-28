from django import forms
from .models import Will, Agreement, AgreementCategory


class DateInput(forms.DateInput):

    input_type = 'date'
    # date_field=forms.DateField(widget=DateInput)


class WillForm(forms.ModelForm):
    """WillForm definition."""
    date_of_execution = forms.DateField(widget=DateInput,required=False)
    date_deposited = forms.DateField(widget=DateInput)

    class Meta:
        model = Will
        fields=['client','lawyer', 'date_of_execution','date_deposited','receipt_number', 'court','internal_depository']

    # TODO: Define form fields here


class AgreementForm(forms.ModelForm):
    """WillForm definition."""
    date_of_execution = forms.DateField(widget=DateInput,required=False)
    date_of_registration = forms.DateField(widget=DateInput)

    class Meta:
        model = Agreement
        fields=['parties','lawyer', 'category','date_of_execution','date_of_registration','internal_depository']


class AgreementCategoryForm(forms.ModelForm):

    class Meta:
        model = AgreementCategory
        fields = ('__all__')
