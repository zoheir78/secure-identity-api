# from django.urls import path
# from .views import (
#     get_identity_by_context,
#     list_user_contexts,
#     list_all_users,
#     user_visibility_rules,
# )

# urlpatterns = [
#     path(
#         "identity/<str:username>/contexts/",
#         list_user_contexts,
#         name="list_user_contexts",
#     ),
#     path(
#         "identity/<str:username>/<str:context>/",
#         get_identity_by_context,
#         name="get_identity_by_context",
#     ),
# ]

# from django.urls import path
# from .views import (
#     get_identity_by_context,
#     list_user_contexts,
#     list_all_users,
#     user_visibility_rules,
# )

# urlpatterns = [
#     path(
#         "identity/<str:username>/contexts/",
#         list_user_contexts,
#         name="list_user_contexts",
#     ),
#     path(
#         "identity/<str:username>/<str:context>/",
#         get_identity_by_context,
#         name="get_identity_by_context",
#     ),
#     path("users/", list_all_users, name="list_all_users"),
#     path(
#         "visibility-rules/<str:username>/",
#         user_visibility_rules,
#         name="user_visibility_rules",
#     ),
# ]


from django.urls import path
from .views import (
    get_identity_by_context,
    list_user_contexts,
    list_all_users,
    user_visibility_rules,
    get_user_info,
)

urlpatterns = [
    path(
        "identity/<str:username>/contexts/",
        list_user_contexts,
        name="list_user_contexts",
    ),
    path(
        "identity/<str:username>/<str:context>/",
        get_identity_by_context,
        name="get_identity_by_context",
    ),
    path(
        "admin/users/",
        list_all_users,
        name="list_all_users",
    ),
    path(
        "admin/users/<str:username>/rules/",
        user_visibility_rules,
        name="user_visibility_rules",
    ),
    path("user/<str:username>/info/", get_user_info, name="get_user_info"),
]
