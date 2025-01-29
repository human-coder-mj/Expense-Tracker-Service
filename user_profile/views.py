from rest_framework import viewsets, permissions
from .serializers import UserSerializer
from django.contrib.auth.models import User

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser] # only admin can request the users