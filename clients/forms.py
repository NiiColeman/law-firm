from django import forms
from .models import Client, ClientCategory
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField
from cases.models import Case
from wills.models import Will

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




class DateInput(forms.DateInput):

    input_type = 'date'
    # date_field=forms.DateField(widget=DateInput)




class ClientCaseForm(forms.ModelForm):
    # category = AutoCompleteSelectField(
    #     channel='category', required=True, help_text="enter category")


    date_added=forms.DateField(widget=DateInput)


    class Meta:
        model = Case
        fields = [ 'name', 'description','category','case_number','suit_number','court','court_number','lawyer','date_added' ,'representative',]


class ClientWillForm(forms.ModelForm):
    date_deposited= forms.DateField(widget=DateInput)
    date_of_execution=  forms.DateField(widget=DateInput)



    class Meta:
        model=Will
        fields=['date_of_execution','date_deposited','internal_depository','receipt_number','court','lawyer']
