from django.urls import path,include
from .views import login_user_view

urlpatterns = [
    path("api/auth/login/", login_user_view, name="login-user"),
]