from rest_framework.routers import DefaultRouter
from api.views import CategoryViewSet, ExpenseViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'expenses', ExpenseViewSet, basename='expense')

urlpatterns = router.urls
