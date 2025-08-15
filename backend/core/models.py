from django.db import models
from django.contrib.auth.models import User


class IdentityProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    legal_name = models.CharField(max_length=255)
    preferred_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class VisibilityRule(models.Model):
    CONTEXT_CHOICES = [
        ("Admin", "Admin"),
        ("Forum", "Forum"),
        ("Student Portal", "Student Portal"),
        ("Public", "Public"),
    ]
    profile = models.ForeignKey(IdentityProfile, on_delete=models.CASCADE)
    context = models.CharField(max_length=50, choices=CONTEXT_CHOICES)
    show_legal_name = models.BooleanField(default=False)
    show_preferred_name = models.BooleanField(default=False)
    show_username = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.profile.user.username} - {self.context}"
