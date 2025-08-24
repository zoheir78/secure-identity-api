from django import forms
from .models import IdentityProfile


class IdentityProfileForm(forms.ModelForm):
    class Meta:
        model = IdentityProfile
        fields = ["legal_name", "preferred_name", "display_username"]
        widgets = {
            "legal_name": forms.TextInput(attrs={"class": "form-control"}),
            "preferred_name": forms.TextInput(attrs={"class": "form-control"}),
            "display_username": forms.TextInput(attrs={"class": "form-control"}),
        }
