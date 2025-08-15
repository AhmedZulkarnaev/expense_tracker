from rest_framework import viewsets, permissions
from expenses.models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from expenses.api.filters import ExpenseFilter


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
