import django_filters
from ..models import Expense


class ExpenseFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="date", lookup_expr="lte")
    category = django_filters.NumberFilter(field_name="category__id")
    is_income = django_filters.BooleanFilter()

    class Meta:
        model = Expense
        fields = ["date_from", "date_to", "category", "is_income"]
