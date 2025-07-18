from rest_framework.routers import DefaultRouter

from server.api.v1.users.views import ProfileViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('profiles', ProfileViewSet, basename='profiles')
