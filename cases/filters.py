import django_filters
from .models import LegalArgument, Case
from django_filters import filters
from django_filters.widgets import RangeWidget, SuffixedMultiWidget


class CaseFilter(django_filters.FilterSet):
    name = filters.CharFilter(label="Case Title")
    description = filters.CharFilter(label="Case Description")
    category__name = filters.CharFilter(label="Category")
    status__title = filters.CharFilter(label="Status")

    year_added = django_filters.NumberFilter(
        field_name='date_added', lookup_expr='year')
    date_between = django_filters.DateFromToRangeFilter(field_name='date_added', lookup_expr='date',
                                                        label='Date (Between)', widget=RangeWidget(attrs={'placeholder': 'YYYY/MM/DD'}))

    class Meta:
        model = Case
        fields = ["name", "description", "date_added", "status", "category"]
