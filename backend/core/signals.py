from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import IdentityProfile, VisibilityRule


@receiver(post_save, sender=User)
def create_identity_profile(sender, instance, created, **kwargs):
    if not created:
        return
    full = f"{instance.first_name or ''} {instance.last_name or ''}".strip()
    IdentityProfile.objects.get_or_create(
        user=instance,
        defaults={
            "legal_name": full,
            "preferred_name": instance.first_name or instance.username,
            "display_username": instance.username,
        },
    )


@receiver(post_save, sender=IdentityProfile)
def create_default_visibility_rules(sender, instance, created, **kwargs):
    if not created:
        return
    defaults = [
        dict(context="Admin",           show_legal_name=True,  show_preferred_name=True,  show_username=False),
        dict(context="Forum",           show_legal_name=False, show_preferred_name=True,  show_username=True),
        dict(context="Student Portal",  show_legal_name=True,  show_preferred_name=True,  show_username=True),
        dict(context="Public",          show_legal_name=False, show_preferred_name=True,  show_username=False),
    ]
    for d in defaults:
        VisibilityRule.objects.get_or_create(profile=instance, context=d["context"], defaults=d)
