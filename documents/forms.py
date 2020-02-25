from django import forms
from .models import Document, DocumentStatus, DocumentRecord


class DateInput(forms.DateInput):

    input_type = 'date'
    # date_field=forms.DateField(widget=DateInput)


class DocumentForm(forms.ModelForm):
    date_added = forms.DateField(widget=DateInput)
    description = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Document
        fields = ['title', 'date_added', 'status', 'description',
                  'category', 'storage_location']


class DocumentRecordForm(forms.ModelForm):

    class Meta:
        model = DocumentRecord
        fields = ['document', 'requested_by', 'approved_by', 'approved']


class RequestDocumentForm(forms.ModelForm):

    class Meta:
        model = DocumentRecord
        fields = ("document",)
