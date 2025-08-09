from rest_framework import serializers
from expenses.models import Category, Expense
from datetime import date


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий (без поля user — он подставляется автоматически)."""

    class Meta:
        model = Category
        fields = ["id", "name"]


class ExpenseSerializer(serializers.ModelSerializer):
    """Сериализатор расходов/доходов."""

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
        required=False,
    )

    class Meta:
        model = Expense
        fields = [
            "id",
            "amount",
            "description",
            "date",
            "is_income",
            "category",
            "category_id",
        ]


class ReportParamsSerializer(serializers.Serializer):
    """Валидатор параметров периода для отчётов.

    Проверяет, что date_from <= date_to, если оба значения указаны.
    """

    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)

    def validate(self, attrs):
        """Гарантирует, что date_from не больше date_to."""
        d_from = attrs.get("date_from")
        d_to = attrs.get("date_to")
        if d_from and d_to and d_from > d_to:
            raise serializers.ValidationError(
                "date_from не может быть больше, чем date_to."
            )
        return attrs
