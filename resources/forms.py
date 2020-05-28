from django import forms
from .models import Book


class DateInput(forms.DateInput):
    input_type = 'date'
    # date_field=forms.DateField(widget=DateInput)


class BookForm(forms.ModelForm):
    date_added = forms.DateField(widget=DateInput)

    class Meta:
        model = Book
        fields = ("title", "date_added", "branch", "category", "shelf_number")
