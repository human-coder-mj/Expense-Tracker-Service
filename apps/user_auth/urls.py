from django.urls import path,include
from .views import login_user_view, logout_user_view

urlpatterns = [
    path("api/auth/login/", login_user_view, name="login-user"),
    path("api/auth/logout/", logout_user_view, name="logout-user"),
]