from django import forms

from .models import Visitor


class VisitorForm(forms.ModelForm):

    class Meta:
        """Meta definition for Visitorform."""

        model = Visitor
        fields = ('name', 'email', 'phone', 'purpose', 'address')
