from django import forms
from .models import Client, ClientCategory


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'address', 'phone', 'added_by', 'category']


class ClientCategoryForm(forms.ModelForm):

    class Meta:
        model = ClientCategory
        fields = ['title']
