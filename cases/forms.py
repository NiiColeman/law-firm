from django import forms
from .models import Case, Category, Status, CaseTask
from lawyers.models import User, Lawyer


class DateInput(forms.DateInput):

    input_type = 'date'
    # date_field=forms.DateField(widget=DateInput)


class CaseTaskForm(forms.ModelForm):
    deadline = forms.DateField(widget=DateInput)

    class Meta:
        model = CaseTask
        fields = ("task", "description", "priority_level", "deadline")


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
    # lawyer = forms.MultipleChoiceField(widget=forms.SelectMultiple(
    #     attrs={'class': 'form-control select2  select2-multiple', 'multiple': 'multiple', 'data-placeholder': 'Select Lawyer'}), choices=User.objects.all().values_list('id', 'first_name'))
    lawyer = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
        attrs={'class': 'select2 mb-3 select2-multiple', 'placeholder': 'Select Lawyers'}), required=True, queryset=Lawyer.objects.all())

    class Meta:
        model = Case
        fields = ("name", "description", "category",
                  "lawyer", "status", 'date_added')
