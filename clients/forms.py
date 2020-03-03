from django import forms
from .models import Client, ClientCategory
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField


class ClientForm(forms.ModelForm):
    # category = AutoCompleteSelectField(
    #     channel='category', required=True, help_text="enter category")

    class Meta:
        model = Client
        fields = ['name', 'email', 'address', 'phone',  'category']


class ClientCategoryForm(forms.ModelForm):

    class Meta:
        model = ClientCategory
        fields = ['title']
