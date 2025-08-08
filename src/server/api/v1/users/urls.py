from rest_framework.routers import DefaultRouter

from django.urls import path

from server.api.v1.users.views import ProfileViewSet, UserViewSet, RegisterView, LoginView
from server.urls import urlpatterns

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('profiles', ProfileViewSet, basename='profiles')

urlpatterns = router.urls + [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
