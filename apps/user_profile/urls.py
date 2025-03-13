from django.urls import path,include
from .views import UserViewSet, register_view, ProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('api/', include((router.urls))),
    path("api/auth/register/", register_view, name="register-user"),
]


