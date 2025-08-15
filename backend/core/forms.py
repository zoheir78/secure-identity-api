# core/forms.py
from django import forms
from .models import IdentityProfile


class IdentityProfileForm(forms.ModelForm):
    class Meta:
        model = IdentityProfile
        fields = ["legal_name", "preferred_name", "username"]
        widgets = {
            "legal_name": forms.TextInput(attrs={"class": "form-control"}),
            "preferred_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
        }
