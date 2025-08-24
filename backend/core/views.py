from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import IdentityProfile, VisibilityRule
from .serializers import (
    IdentityProfileSerializer,
    VisibilityRuleSerializer,
    UserMinSerializer,
)


# ------------------------
# Current User Endpoint (/api/me/)
# ------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Return details about the currently authenticated user.
    Includes username, admin status, and profile ID.
    """
    user = request.user
    profile = get_object_or_404(IdentityProfile, user=user)
    return Response({
        "id": user.id,
        "username": user.username,
        "is_staff": user.is_staff,
        "profileId": profile.id,   #  use camelCase to match frontend
    })


# ------------------------
# Permissions
# ------------------------
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Authenticated users can read; only staff can write.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)


# ------------------------
# IdentityProfile ViewSet
# ------------------------
class IdentityProfileViewSet(viewsets.ModelViewSet):
    queryset = IdentityProfile.objects.select_related("user").all()
    serializer_class = IdentityProfileSerializer
    permission_classes = [IsAdminOrReadOnly]

    # GET /api/profiles/{id}/contexts/
    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def contexts(self, request, pk=None):
        profile = self.get_object()
        contexts = list(
            VisibilityRule.objects.filter(profile=profile).values_list("context", flat=True)
        )
        return Response({"contexts": contexts}, status=status.HTTP_200_OK)

    # GET /api/profiles/{id}/identity/?context=Forum
    # Note: Allow unauthenticated access ONLY for Public context.
    @action(detail=True, methods=["get"], permission_classes=[permissions.AllowAny])
    def identity(self, request, pk=None):
        profile = self.get_object()
        context = request.query_params.get("context")

        if not context:
            return Response({"error": "Context is required"}, status=status.HTTP_400_BAD_REQUEST)

        if context.lower() != "public" and not request.user.is_authenticated:
            return Response({"detail": "Authentication required for this context."}, status=status.HTTP_401_UNAUTHORIZED)

        rule = VisibilityRule.objects.filter(
            profile=profile, context__iexact=context
        ).first()
        if not rule:
            return Response({"error": "No visibility rule for this context"}, status=status.HTTP_404_NOT_FOUND)

        data = {}
        if rule.show_legal_name:
            data["legal_name"] = profile.legal_name
        if rule.show_preferred_name:
            data["preferred_name"] = profile.preferred_name
        if rule.show_username:
            data["username"] = profile.display_username or profile.user.username  

        return Response(data, status=status.HTTP_200_OK)


# ------------------------
# VisibilityRule ViewSet
# ------------------------
class VisibilityRuleViewSet(viewsets.ModelViewSet):
    queryset = VisibilityRule.objects.select_related("profile", "profile__user").all()
    serializer_class = VisibilityRuleSerializer
    permission_classes = [IsAdminOrReadOnly]

    # Enable filtering rules by profileId
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["profile"]


# ------------------------
# User ViewSet (Read-only, admin only)
# ------------------------
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserMinSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    # GET /api/users/{id}/info/
    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def info(self, request, pk=None):
        user = self.get_object()
        return Response({"username": user.username, "is_staff": user.is_staff})
