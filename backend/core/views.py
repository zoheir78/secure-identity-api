from rest_framework.decorators import api_view, permission_classes

# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import IdentityProfile, VisibilityRule


from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated, IsAdminUser

# from rest_framework.response import Response
# from .models import IdentityProfile, VisibilityRule
from .serializers import IdentityProfileSerializer


#  List all users
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def list_all_users(request):
    users = User.objects.all().values("id", "username")
    return Response(list(users))


# Get and update visibility rules for a user
@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated, IsAdminUser])
def user_visibility_rules(request, username):
    try:
        profile = IdentityProfile.objects.get(user__username=username)
    except IdentityProfile.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    if request.method == "GET":
        rules = VisibilityRule.objects.filter(profile=profile).values(
            "id", "context", "show_legal_name", "show_preferred_name", "show_username"
        )
        return Response(list(rules))

    if request.method == "PUT":
        data = request.data
        for rule_data in data:
            try:
                rule = VisibilityRule.objects.get(id=rule_data["id"], profile=profile)
                rule.show_legal_name = rule_data["show_legal_name"]
                rule.show_preferred_name = rule_data["show_preferred_name"]
                rule.show_username = rule_data["show_username"]
                rule.save()
            except VisibilityRule.DoesNotExist:
                continue
        return Response({"status": "updated"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_identity_by_context(request, username, context):
    try:
        profile = IdentityProfile.objects.get(user__username=username)
    except IdentityProfile.DoesNotExist:
        return Response(
            {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
        )

    # case-insensitive match, and avoid exceptions if multiple entries exist
    rule = VisibilityRule.objects.filter(
        profile=profile, context__iexact=context
    ).first()
    if not rule:
        return Response(
            {"error": "No visibility rule for this context"},
            status=status.HTTP_404_NOT_FOUND,
        )

    data = {}
    if rule.show_legal_name:
        data["legal_name"] = profile.legal_name
    if rule.show_preferred_name:
        data["preferred_name"] = profile.preferred_name
    if rule.show_username:
        data["username"] = profile.username

    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_user_contexts(request, username):
    try:
        profile = IdentityProfile.objects.get(user__username=username)
    except IdentityProfile.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    contexts = VisibilityRule.objects.filter(profile=profile).values_list(
        "context", flat=True
    )
    return Response({"contexts": list(contexts)}, status=status.HTTP_200_OK)


# check whether the current user is an admin.
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_info(request, username):
    try:
        user = User.objects.get(username=username)
        return Response(
            {"username": user.username, "is_staff": user.is_staff}  # True if admin
        )
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
