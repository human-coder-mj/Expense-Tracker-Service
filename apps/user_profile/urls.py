from django.urls import path,include
from .views import  register_user_view, delete_user_view , ProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('api/', include((router.urls))),
    path("api/user/register/", register_user_view, name="register-user"),
    path("api/user/delete/", delete_user_view, name="delete-user"),
]


