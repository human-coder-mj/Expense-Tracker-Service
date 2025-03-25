from django.urls import path,include
from .views import BudgetViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'budget', BudgetViewSet, basename='budget')

urlpatterns = [
    path('api/user/', include((router.urls))),
]