from rest_framework import serializers
from expenses.models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий (без поля user — он подставляется автоматически)."""

    class Meta:
        model = Category
        fields = ['id', 'name']


class ExpenseSerializer(serializers.ModelSerializer):
    """Сериализатор расходов/доходов."""

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )

    class Meta:
        model = Expense
        fields = ['id', 'amount', 'description', 'date', 'is_income', 'category', 'category_id']