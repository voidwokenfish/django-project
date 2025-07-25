import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, viewsets

from server.api.core.pagination.base import StandardPagePagination
from server.api.v1.news.serializers import NewsSerializer, NewsWriteSerializer
from server.apps.news.models import News, NewsImage


class NewsFilter(django_filters.FilterSet):
    """Фильтры для вьюсета новостей"""

    id = django_filters.CharFilter(lookup_expr='iexact')
    notification_status = django_filters.CharFilter(lookup_expr='icontains')
    pub_date = django_filters.CharFilter(lookup_expr='icontains')
    is_published = django_filters.BooleanFilter()

    class Meta:
        model = News
        fields = ['id', 'notification_status', 'pub_date', 'is_published']


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.filter().order_by('id')
    serializer_class = NewsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = StandardPagePagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_class = NewsFilter
    ordering_fields = ['id', 'pub_date', 'notification_status', 'is_published']
    search_fields = ('title', 'id',)

    def get_queryset(self):
        """Переопределяем """

        if self.action in ('create', 'update', 'partial_update'):
            return NewsWriteSerializer
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