from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import IdentityProfile, VisibilityRule


# Step 1: Create IdentityProfile automatically when a new User is created
@receiver(post_save, sender=User)
def create_identity_profile(sender, instance, created, **kwargs):
    if created:
        full = f"{instance.first_name or ''} {instance.last_name or ''}".strip()
        IdentityProfile.objects.create(
            user=instance,
            legal_name=full if full else "",  # blank if not provided
            preferred_name=instance.first_name or "",  # prefer first_name over username
            username=instance.username,
        )


# Step 2: Create default visibility rules when an IdentityProfile is created
@receiver(post_save, sender=IdentityProfile)
def create_default_visibility_rules(sender, instance, created, **kwargs):
    if created:
        default_rules = [
            {
                "context": "Admin",
                "show_legal_name": True,
                "show_preferred_name": True,
                "show_username": False,
            },
            {
                "context": "Forum",
                "show_legal_name": False,
                "show_preferred_name": True,
                "show_username": True,
            },
            {
                "context": "Student Portal",
                "show_legal_name": True,
                "show_preferred_name": True,
                "show_username": True,
            },
            {
                "context": "Public",
                "show_legal_name": False,
                "show_preferred_name": True,
                "show_username": False,
            },
        ]
        for rule in default_rules:
            VisibilityRule.objects.create(profile=instance, **rule)
