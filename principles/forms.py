from django import forms
from .models import Authority, Principles


class AuthorityForm(forms.ModelForm):
    class Meta:
        model = Authority
        fields = ['title']


class PrinciplesForm(forms.ModelForm):
    class Meta:
        model = Principles

        fields = ['principle', 'authority', 'description']
