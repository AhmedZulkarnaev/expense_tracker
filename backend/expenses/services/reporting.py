from django.db.models import Sum, Q, DecimalField, Value
from django.db.models.functions import Coalesce
from expenses.models import Expense


DECIMAL = DecimalField(max_digits=12, decimal_places=2)


def _base_qs(user, date_from=None, date_to=None):
    qs = Expense.objects.filter(user=user)
    if date_from:
        qs = qs.filter(date__gte=date_from)
    if date_to:
        qs = qs.filter(date__lte=date_to)
    return qs


def get_summary(user, date_from=None, date_to=None):
    """
    Возвращает:
    {
      "income_total": Decimal,
      "expense_total": Decimal,
      "balance": Decimal
    }
    """
    qs = _base_qs(user, date_from, date_to)

    agg = qs.aggregate(
        income_total=Coalesce(
            Sum("amount", filter=Q(is_income=True)),
            Value(0, output_field=DECIMAL),
        ),
        expense_total=Coalesce(
            Sum("amount", filter=Q(is_income=False)),
            Value(0, output_field=DECIMAL),
        ),
    )

    income_total = agg["income_total"]
    expense_total = agg["expense_total"]
    balance = income_total - expense_total

    return {
        "income_total": income_total,
        "expense_total": expense_total,
        "balance": balance,
    }


def get_by_category(user, date_from=None, date_to=None):
    """
    Возвращает список:
    [
      { "category": "Еда", "income": Decimal, "expense": Decimal },
      ...
    ]
    """
    qs = _base_qs(user, date_from, date_to).select_related("category")

    rows = (
        qs.values("category_id", "category__name")
        .annotate(
            income=Coalesce(
                Sum("amount", filter=Q(is_income=True)),
                Value(0, output_field=DECIMAL),
            ),
            expense=Coalesce(
                Sum("amount", filter=Q(is_income=False)),
                Value(0, output_field=DECIMAL),
            ),
        )
        .order_by("category__name")
    )

    result = []
    for r in rows:
        name = r["category__name"] or "Без категории"
        result.append(
            {
                "category": name,
                "income": r["income"],
                "expense": r["expense"],
            }
        )
    return result
