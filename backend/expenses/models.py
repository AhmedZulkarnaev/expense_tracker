from django.db import models
from django.conf import settings


class Category(models.Model):
    """
    Категория расходов (например: еда, транспорт).
    Уникальна в пределах пользователя.
    """
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name', 'user']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Expense(models.Model):
    """
    Расход или доход, привязанный к пользователю и категории.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    is_income = models.BooleanField(default=False)

    def __str__(self):
        return f"{'Доход' if self.is_income else 'Расход'}: {self.amount}"
