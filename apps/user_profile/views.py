from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import viewsets, permissions, status, parsers
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.request import Request
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from .models import Profile
from .utils import get_refresh_tokens 
from .serializers import UserSerializer, ProfileSerializer, ChangePasswordSerializer
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError

@api_view(["Post"])
def register_user_view(request):
    
    register_serializer = UserSerializer(data=request.data)

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

@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_user_view(request: Request) -> Response:
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    user.delete()
    return Response({"detail": "User has been deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT)



class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser]

    def get_queryset(self):
        """
        Limits the queryset to only the profile of the authenticated user.
        Prevents users from accessing other profiles.
        """
        return Profile.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        Handles GET request to fetch the profile of the authenticated user.
        """
        
        profile = self.get_queryset().first()
        if not profile:
            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Handles PUT request to update the profile of the authenticated user.
        Supports updating profile picture and other fields.
        """
        profile = self.get_queryset().first()
        if not profile:
            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = request.data.copy()
        data['user'] = request.user.pk  # Ensure user field remains correct
        serializer = self.get_serializer(profile, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Handles DELETE request to allow the authenticated user to delete their profile.
        """
        profile = self.get_queryset().first()
        if not profile:
            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        profile.delete()
        return Response(
            {"detail": "Profile has been deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['get'], url_path='me')
    def get_own_profile(self, request):
        """
        Custom action: Handles GET request to retrieve the authenticated user's profile.
        """
        return self.retrieve(request)
    
@api_view(http_method_names=['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password_view(request: Request) -> Response:
    """
    Allows an authenticated user to change their password.
    Ensures the old password is correct and enforces password security.
    """
    user = request.user
    serializer = ChangePasswordSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    old_password = serializer.validated_data.get("old_password")
    new_password = serializer.validated_data.get("new_password")

    if new_password == old_password:
        return Response({"error": "New password cannot be the same as the old password."},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    if not user.check_password(old_password):
        return Response({"error": "Incorrect old password."},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    try:
        validate_password(new_password, user=user)  # Django's built-in validation
    except ValidationError as e:
        return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    update_session_auth_hash(request, user)

    return Response({'detail': 'Your password has been successfully changed.'},
                    status=status.HTTP_200_OK)