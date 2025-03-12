from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from .models import Profile
from .utils import get_refresh_tokens 
from .serializers import UserSerializer, RegistrationSerializer, ProfileSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser] # only admin can request the users


@api_view(["Post"])
def register_view(request):
    
    register_serializer = RegistrationSerializer(data=request.data)

    if register_serializer.is_valid():
        user = register_serializer.save()

        token_serializer = TokenObtainSerializer(data=request.data)
        if token_serializer.is_valid():
            profile = Profile.objects.filter(user=user).first()
            profile_serializer = ProfileSerializer(profile, many=False)

            tokens = get_refresh_tokens(user)

            return Response(
                {'profile': profile_serializer.data, 'tokens': tokens},
                status=status.HTTP_201_CREATED
            )

        return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names=["GET"])
def get_users_profile(request: Request) -> Response:

    profile = Profile.objects.get(user=request.user)
    profile_serializer = ProfileSerializer(profile, many=False)
    return Response(profile_serializer.data, status=status.HTTP_200_OK)
