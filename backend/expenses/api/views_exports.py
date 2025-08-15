from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import HttpRequest
from expenses.models import Expense
from .filters import ExpenseFilter
from expenses.services.exporters import export_expenses_csv
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes


@extend_schema(
    summary="Экспорт расходов/доходов в CSV",
    description="Выгружает отфильтрованный список операций в формате CSV. "
    "Поддерживает те же параметры фильтрации, что и список расходов.",
    parameters=[
        OpenApiParameter(
            "date_from",
            OpenApiTypes.DATE,
            OpenApiParameter.QUERY,
            description="Начало периода",
        ),
        OpenApiParameter(
            "date_to",
            OpenApiTypes.DATE,
            OpenApiParameter.QUERY,
            description="Конец периода",
        ),
        OpenApiParameter(
            "category",
            OpenApiTypes.INT,
            OpenApiParameter.QUERY,
            description="ID категории",
        ),
        OpenApiParameter(
            "is_income",
            OpenApiTypes.BOOL,
            OpenApiParameter.QUERY,
            description="true=доход, false=расход",
        ),
        OpenApiParameter(
            "ordering",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            description="date или amount, с префиксом - для убывания",
        ),
    ],
    responses={
        200: OpenApiResponse(description="CSV файл (text/csv)"),
        401: OpenApiResponse(description="Требуется аутентификация"),
    },
)
class ExportExpensesCSVView(APIView):
    """Экспорт расходов/доходов в CSV с теми же фильтрами, что в списке."""

    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest):
        base_qs = Expense.objects.filter(user=request.user).select_related("category")
        qs = ExpenseFilter(request.GET, queryset=base_qs).qs
        return export_expenses_csv(qs)
