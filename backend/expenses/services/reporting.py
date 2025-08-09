from django.db.models import Sum, Case, When, DecimalField, Value
from django.db.models.functions import Coalesce
from expenses.models import Expense, Category


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

    income_total = qs.aggregate(
        s=Coalesce(
            Sum(
                Case(
                    When(is_income=True, then="amount"),
                    default=Value(0),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            ),
            Value(0),
        )
    )["s"]

    expense_total = qs.aggregate(
        s=Coalesce(
            Sum(
                Case(
                    When(is_income=False, then="amount"),
                    default=Value(0),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            ),
            Value(0),
        )
    )["s"]

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
                Sum(
                    Case(
                        When(is_income=True, then="amount"),
                        default=Value(0),
                        output_field=DecimalField(max_digits=10, decimal_places=2),
                    )
                ),
                Value(0),
            ),
            expense=Coalesce(
                Sum(
                    Case(
                        When(is_income=False, then="amount"),
                        default=Value(0),
                        output_field=DecimalField(max_digits=10, decimal_places=2),
                    )
                ),
                Value(0),
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
