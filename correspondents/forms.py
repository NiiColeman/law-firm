from django import forms
from .models import Correspondent


class DateInput(forms.DateInput):

    input_type = 'date'
    # date_field=


class CorrespondentForm(forms.ModelForm):
    """Form definition for Correspondent."""
    date_added = forms.DateField(widget=DateInput)
    correspondents=forms.CharField(label="Correspondence")

    class Meta:
        """Meta definition for Correspondentform."""

        model = Correspondent
        fields = ('title', 'case', 'clients', 'description', 'date_added',)


class CaseCorrespondentForm(forms.ModelForm):
    """Form definition for Correspondent."""
    date_added = forms.DateField(widget=DateInput)
    correspondents=forms.CharField(label="Correspondence")

    class Meta:
        """Meta definition for Correspondentform."""

        model = Correspondent
        fields = ('title', 'description', 'date_added',
                  )
