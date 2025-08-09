from rest_framework import viewsets, permissions
from expenses.models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from expenses.filters import ExpenseFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ReportParamsSerializer
from expenses.services.reporting import get_summary, get_by_category


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Категории пользователя. Только его собственные.
    """

    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    Расходы/доходы пользователя. Только его собственные.
    """

    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ExpenseFilter
    ordering_fields = ["date", "amount"]
    ordering = ["-date"]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
