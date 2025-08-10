from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    CategoryViewSet,
    ExpenseViewSet,
)
from api.views_reports import (
    SummaryReportView,
    ByCategoryReportView,
)
from api.views_exports import ExportExpensesCSVView

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"expenses", ExpenseViewSet, basename="expense")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "exports/expenses.csv",
        ExportExpensesCSVView.as_view(),
        name="export-expenses-csv",
    ),
    path("reports/summary/", SummaryReportView.as_view(), name="report-summary"),
    path(
        "reports/by-category/",
        ByCategoryReportView.as_view(),
        name="report-by-category",
    ),
]
