from rest_framework import serializers
from django.contrib.auth.models import User
from .models import IdentityProfile, VisibilityRule


class UserMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff"]


class IdentityProfileSerializer(serializers.ModelSerializer):
    user = UserMinSerializer(read_only=True)

    class Meta:
        model = IdentityProfile
        fields = ["id", "user", "legal_name", "preferred_name", "display_username"]


class VisibilityRuleSerializer(serializers.ModelSerializer):
    profile_id = serializers.PrimaryKeyRelatedField(
        source="profile", queryset=IdentityProfile.objects.all(), write_only=True, required=False
    )
    profile = IdentityProfileSerializer(read_only=True)

    class Meta:
        model = VisibilityRule
        fields = [
            "id",
            "profile",
            "profile_id",        # optional when creating/updating as admin
            "context",
            "show_legal_name",
            "show_preferred_name",
            "show_username",
        ]
