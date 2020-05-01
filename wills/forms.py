from django import forms
from .models import Will, Agreement, AgreementCategory


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


class AgreementForm(forms.ModelForm):
    """WillForm definition."""
    date_of_execution = forms.DateField(widget=DateInput)
    date_of_registration = forms.DateField(widget=DateInput)

    class Meta:
        model = Agreement
        exclude = ('user',)


class AgreementCategoryForm(forms.ModelForm):

    class Meta:
        model = AgreementCategory
        fields = ('__all__')
