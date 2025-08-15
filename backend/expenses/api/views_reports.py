from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ReportParamsSerializer
from expenses.services.reporting import get_summary, get_by_category

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)
from drf_spectacular.types import OpenApiTypes

date_from_param = OpenApiParameter(
    name="date_from",
    type=OpenApiTypes.DATE,
    location=OpenApiParameter.QUERY,
    description="Начало периода (YYYY-MM-DD). Необязательный.",
)
date_to_param = OpenApiParameter(
    name="date_to",
    type=OpenApiTypes.DATE,
    location=OpenApiParameter.QUERY,
    description="Конец периода (YYYY-MM-DD). Необязательный.",
)


@extend_schema(
    summary="Итоги за период",
    description="Считает суммы доходов, расходов и баланс за выбранный период.",
    parameters=[date_from_param, date_to_param],
    responses={
        200: OpenApiResponse(
            description="ОК",
            examples=[
                OpenApiExample(
                    "Пример",
                    value={
                        "income_total": "1200.00",
                        "expense_total": "800.00",
                        "balance": "400.00",
                    },
                )
            ],
        ),
        401: OpenApiResponse(description="Требуется аутентификация"),
        400: OpenApiResponse(
            description="Неверные параметры (например, date_from > date_to)"
        ),
    },
)
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


@extend_schema(
    summary="Суммы по категориям",
    description="Возвращает суммы доходов и расходов, сгруппированные по категориям, за период.",
    parameters=[date_from_param, date_to_param],
    responses={
        200: OpenApiResponse(
            description="ОК",
            examples=[
                OpenApiExample(
                    "Пример",
                    value=[
                        {"category": "Еда", "income": "0.00", "expense": "250.00"},
                        {
                            "category": "Зарплата",
                            "income": "1200.00",
                            "expense": "0.00",
                        },
                    ],
                )
            ],
        ),
        401: OpenApiResponse(description="Требуется аутентификация"),
        400: OpenApiResponse(description="Неверные параметры"),
    },
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
