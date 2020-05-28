from django import forms
from .models import Case, Category, Status, CaseTask, CaseFile, CaseArchive, LegalArgument, Court,CourtSession,Representative,Process

from lawyers.models import User, Lawyer
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField


class DateInput(forms.DateInput):

    input_type = 'date'
    # date_field=forms.DateField(widget=DateInput)


class CaseTaskForm(forms.ModelForm):
    deadline = forms.DateField(widget=DateInput)

    class Meta:
        model = CaseTask
        fields = ("task", "description", "deadline")


# choice=User.objects.a

class CaseForm(forms.ModelForm):
    # attachments = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
    #     'multiple': True
    # }))

    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    description = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'elm1'}))
    date_added = forms.DateField(widget=DateInput(
        attrs={'class': 'form-control', 'id': 'date-format'}))
    representative = forms.ModelChoiceField(
        queryset=Representative.objects.all(), label="Representation")
    # lawyer = forms.MultipleChoiceField(widget=forms.SelectMultiple(
    #     attrs={'class': 'form-control select2  select2-multiple', 'multiple': 'multiple', 'data-placeholder': 'Select Lawyer'}), choices=User.objects.all().values_list('id', 'first_name'))

    class Meta:
        model = Case
        fields = ("name", "client", "description", "lawyer", "category","representative","court","case_number","court_number","suit_number",
                   'date_added')


class CaseFileForm(forms.ModelForm):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = CaseFile
        fields = ("file",)


class CaseArchiveForm(forms.ModelForm):

    class Meta:
        model = CaseArchive
        fields = ('archive_location',)


class CaseForms(forms.ModelForm):
    description = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'class': 'form-control'}))
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    # representative = forms.CharField(required=True, label="Representation", widget=forms.TextInput(
    #     attrs={'class': 'form-control'}))

    date_added = forms.DateField(widget=DateInput(
        attrs={'class': 'form-control'}))
    representative = forms.ModelChoiceField(
        queryset=Representative.objects.all(), label="Representation")

    class Meta:
        model = Case
        fields = ['name', 'client', 'description',  'category','case_number', 'representative', 'court_number', 'suit_number',
                  'lawyer', 'date_added', 'court']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', ]


class LegalArgumentForm(forms.ModelForm):
    class Meta:
        model = LegalArgument
        fields = ['argument', 'authorities']


class CourtForm(forms.ModelForm):

    class Meta:
        model = Court
        fields = ("name",)


class CourtSessionForm(forms.ModelForm):
    purpose = forms.CharField(required=True, label='Purpose/Court Remarks', widget=forms.Textarea(
        attrs={'class': 'form-control'}))

    class Meta:
        model = CourtSession
        fields = ("purpose",)



class ProcessForm(forms.ModelForm):

    class Meta:
        model = Process
        fields =('case', 'process',)


