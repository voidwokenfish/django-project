from server.api.v1.courses.serializers import CourseListSerializer, CourseDetailSerializer, CourseWriteSerializer
from rest_framework import viewsets, filters
from server.apps.courses.models import Course
from rest_framework import permissions
from server.api.core.pagination.base import StandardPagePagination


class CourseViewSet(viewsets.ModelViewSet):
    """Вьюсет для CRUD операций над моделью курсов"""
    queryset = Course.objects.filter(is_active=True).order_by('title')
    serializer_class = CourseListSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardPagePagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    ordering_fields = ('id', 'title', 'price')
    search_fields = ('id', 'title')

    def get_serializer_class(self):
        """Переопределяем """
        if self.action in ('create', 'update', 'partial_update',):
            return CourseWriteSerializer
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return self.serializer_class
