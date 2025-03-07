from django.urls import path,include
from .views import UserViewSet, RegisterUserViewSet, get_users_profile
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path('api/', include((router.urls))),
    path("api/auth/register/", RegisterUserViewSet.as_view({"post": "create"}), name="register-user"),
    path("api/user/profile", get_users_profile, name="user-profile"),
]


