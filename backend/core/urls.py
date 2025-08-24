from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IdentityProfileViewSet, VisibilityRuleViewSet, UserViewSet, current_user

router = DefaultRouter()
router.register(r'profiles', IdentityProfileViewSet, basename='profiles')
router.register(r'rules', VisibilityRuleViewSet, basename='rules')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),        #  /api/profiles/, /api/rules/, /api/users/
    path('me/', current_user, name="me"),  #  /api/me/
]
