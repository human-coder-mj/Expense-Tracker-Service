from django.urls import path,include
from .views import BudgetViewSet, GoalViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'budget', BudgetViewSet, basename='budget')
router.register(r'goal', GoalViewSet, basename='goal')

urlpatterns = [
    path('api/user/', include((router.urls))),
]