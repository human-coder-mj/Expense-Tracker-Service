from rest_framework import viewsets, permissions, views
from .serializers import UserSerializer, RegistrationSerializer, ProfileSerializer
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework import status

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser] # only admin can request the users


class RegisterUserViewSet(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response({
            "profile": RegistrationSerializer(profile, context=self.get_serializer_context()).data
        })


@api_view(http_method_names=["GET"])
def get_users_profile(request: Request) -> Response:

    profile = Profile.objects.get(user=request.user)
    profile_serializer = ProfileSerializer(profile, many=False)
    return Response(profile_serializer.data, status=status.HTTP_200_OK)
