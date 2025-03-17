from django.urls import path,include
from .views import  register_user_view, delete_user_view , ProfileViewSet, change_password_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('api/', include((router.urls))),
    path("api/user/register/", register_user_view, name="register-user"),
    path("api/user/delete/", delete_user_view, name="delete-user"),
    path("api/user/change_password/", change_password_view, name="change-password"),
]


