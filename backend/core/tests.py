
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from core.models import IdentityProfile, VisibilityRule
from core.serializers import IdentityProfileSerializer, VisibilityRuleSerializer


# -------------------------
# Model Tests
# -------------------------
class IdentityProfileModelTest(TestCase):
    def test_identity_profile_str(self):
        user, _ = User.objects.get_or_create(username="john", defaults={"password": "password123"})
        profile, _ = IdentityProfile.objects.get_or_create(
            user=user,
            defaults={
                "legal_name": "John Doe",
                "preferred_name": "Johnny",
                "username": "john123",
            },
        )
        self.assertEqual(str(profile), "john")


class VisibilityRuleModelTest(TestCase):
    def test_visibility_rule_str(self):
        user, _ = User.objects.get_or_create(username="alice", defaults={"password": "password123"})
        profile, _ = IdentityProfile.objects.get_or_create(
            user=user,
            defaults={
                "legal_name": "Alice Wonderland",
                "preferred_name": "Ally",
                "username": "alice123",
            },
        )
        rule = VisibilityRule.objects.create(
            profile=profile,
            context="Forum",
            show_legal_name=False,
            show_preferred_name=True,
            show_username=True,
        )
        self.assertEqual(str(rule), "alice - Forum")

