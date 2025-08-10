from typing import Iterable
from django.http import HttpResponse
import csv
from expenses.models import Expense


def export_expenses_csv(qs: Iterable[Expense]) -> HttpResponse:
    """Сформировать CSV из расходов/доходов. Колонки: date, amount, type, category, description."""

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="expenses.csv"'
    writer = csv.writer(response)
    writer.writerow(["date", "amount", "type", "category", "description"])
    for e in qs:
        writer.writerow(
            [
                e.date.isoformat(),
                f"{e.amount:.2f}",
                "income" if e.is_income else "expense",
                e.category.name if e.category else "",
                (e.description or "").replace("\n", " ").strip(),
            ]
        )
    return response
