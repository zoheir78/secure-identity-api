from django.contrib import admin
from .models import IdentityProfile, VisibilityRule


@admin.register(IdentityProfile)
class IdentityProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "legal_name", "preferred_name", "display_username")
    search_fields = ("user__username", "legal_name", "preferred_name", "display_username")


@admin.register(VisibilityRule)
class VisibilityRuleAdmin(admin.ModelAdmin):
    list_display = ("profile", "context", "show_legal_name", "show_preferred_name", "show_username")
    list_filter = ("context",)
    search_fields = ("profile__user__username",)
