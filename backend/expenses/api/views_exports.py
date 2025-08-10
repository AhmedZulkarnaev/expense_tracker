from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import HttpRequest
from expenses.models import Expense
from .filters import ExpenseFilter
from expenses.services.exporters import export_expenses_csv


class ExportExpensesCSVView(APIView):
    """Экспорт расходов/доходов в CSV с теми же фильтрами, что в списке."""

    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest):
        base_qs = Expense.objects.filter(user=request.user).select_related("category")
        qs = ExpenseFilter(request.GET, queryset=base_qs).qs
        return export_expenses_csv(qs)
