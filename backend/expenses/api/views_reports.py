from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ReportParamsSerializer
from expenses.services.reporting import get_summary, get_by_category


class SummaryReportView(APIView):
    """
    Отчёт: итоговые суммы (доходы, расходы, баланс) за период.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        params = ReportParamsSerializer(data=request.query_params)
        params.is_valid(raise_exception=True)
        data = get_summary(
            user=request.user,
            date_from=params.validated_data.get("date_from"),
            date_to=params.validated_data.get("date_to"),
        )
        return Response(
            {
                "income_total": str(data["income_total"]),
                "expense_total": str(data["expense_total"]),
                "balance": str(data["balance"]),
            }
        )


class ByCategoryReportView(APIView):
    """
    Отчёт: суммы по категориям (доходы/расходы) за период.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        params = ReportParamsSerializer(data=request.query_params)
        params.is_valid(raise_exception=True)
        data = get_by_category(
            user=request.user,
            date_from=params.validated_data.get("date_from"),
            date_to=params.validated_data.get("date_to"),
        )
        normalized = [
            {
                "category": r["category"],
                "income": str(r["income"]),
                "expense": str(r["expense"]),
            }
            for r in data
        ]
        return Response(normalized)
