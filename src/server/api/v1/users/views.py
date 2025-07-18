import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from server.api.core.pagination.base import StandardPagePagination
from server.api.v1.users.serializers import (ProfileSerializer,
                                             UserDetailSerializer,
                                             UserListSerializer,
                                             UserWriteSerializer)
from server.apps.users.models import Profile, User


class UserFilter(django_filters.FilterSet):
    """Фильтры для вьюсета пользователя"""

    id = django_filters.CharFilter(lookup_expr='iexact')
    email = django_filters.CharFilter(lookup_expr='iexact')
    username = django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_active']


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для CRUD операций над моделью пользователя"""

    queryset = User.objects.filter().order_by('id')
    serializer_class = UserListSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardPagePagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = UserFilter
    ordering_fields = ['id', 'email', 'username', 'is_active']
    search_fields = ('id', 'username', 'email',)

    def get_serializer_class(self):
        """Переопределяем """
        if self.action in ("create", "update", "partial_update"):
            return UserWriteSerializer
        if self.action == "retrieve":
            return UserDetailSerializer
        return self.serializer_class

    @swagger_auto_schema(
        operation_description="Получить список пользователей с фильтрацией",
        manual_parameters=[
            openapi.Parameter(
                'is_active', openapi.IN_QUERY,
                description='Фильтр по активности (true / false)',
                type=openapi.TYPE_BOOLEAN
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProfileViewSet(viewsets.ModelViewSet):
    """Вьюсет для CRUD операций над моделью пользователя"""

    queryset = Profile.objects.filter().order_by('id')
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardPagePagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    ordering_fields = ('id',)
    search_fields = ('id', 'user',)
