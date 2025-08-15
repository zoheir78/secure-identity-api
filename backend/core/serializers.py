from rest_framework import serializers
from .models import IdentityProfile, VisibilityRule


class IdentityProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentityProfile
        fields = ["id", "user", "legal_name", "preferred_name", "username"]


class VisibilityRuleSerializer(serializers.ModelSerializer):
    profile = IdentityProfileSerializer(read_only=True)

    class Meta:
        model = VisibilityRule
        fields = [
            "id",
            "profile",
            "context",
            "show_legal_name",
            "show_preferred_name",
            "show_username",
        ]
