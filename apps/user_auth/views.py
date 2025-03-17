from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from user_profile.models import Profile
from user_profile.serializers import ProfileSerializer
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from user_profile.utils import get_refresh_tokens  

@api_view(["POST"])
def login_user_view(request):
    """
    Handles user login and returns JWT tokens.
    """
    login_serializer = TokenObtainSerializer(data=request.data)

    if not login_serializer.is_valid():
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    user = login_serializer.user

    # Authenticate user to ensure correct password is provided
    authenticated_user = authenticate(
        username=user.username, password=request.data.get("password")
    )

    if not authenticated_user:
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Get the user's profile
    try:
        profile = Profile.objects.get(user=user)
        profile_serializer = ProfileSerializer(profile)
    except Profile.DoesNotExist:
        return Response(
            {"error": "User profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Generate JWT tokens
    tokens = get_refresh_tokens(user)

    return Response(
        {
            "message": "Login successful",
            "profile": profile_serializer.data,
            "tokens": tokens
        },
        status=status.HTTP_200_OK
    )
