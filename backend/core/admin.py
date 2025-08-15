from django.contrib import admin
from .models import IdentityProfile, VisibilityRule

admin.site.register(IdentityProfile)
admin.site.register(VisibilityRule)
