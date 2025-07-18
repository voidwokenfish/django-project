from rest_framework import filters, permissions, viewsets

from server.api.core.pagination.base import StandardPagePagination
from server.api.v1.courses.serializers import (CourseDetailSerializer,
                                               CourseListSerializer,
                                               CourseWriteSerializer,
                                               EnrollmentSerializer,
                                               LessonDetailSerializer,
                                               LessonListSerializer,
                                               LessonWriteSerializer,
                                               ModuleDetailSerializer,
                                               ModuleListSerializer,
                                               ModuleWriteSerializer)
from server.apps.courses.models import Course, Enrollment, Lesson, Module


class LessonViewSet(viewsets.ModelViewSet):
    """Вьюсет для CRUD операций над моделью урока"""

    queryset = Lesson.objects.filter().order_by('title')
    serializer_class = LessonListSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardPagePagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    ordering_fields = ('id', 'title', 'module')
    search_fields = ('id', 'title')

    def get_serializer_class(self):
        """Переопределяем """
        if self.action in ("create", "update", "partial_update"):
            return LessonWriteSerializer
        if self.action == "retrieve":
            return LessonDetailSerializer
        return self.serializer_class


class ModuleViewSet(viewsets.ModelViewSet):
    """Вьюсет для CRUD операция над моделью модуля"""

    queryset = Module.objects.filter().order_by('title')
    serializer_class = ModuleListSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardPagePagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    ordering_fields = ('id', 'title', 'course')
    search_fields = ('id', 'title')

    def get_serializer_class(self):
        """Переопределяем """

        if self.action in ("create", "update", "partial_update"):
            return ModuleWriteSerializer
        if self.action == "retrieve":
            return ModuleDetailSerializer
        return self.serializer_class


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


class EnrollmentViewSet(viewsets.ModelViewSet):
    """Вьюсет для CRUD операций над моделью зачислений"""

    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = StandardPagePagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    ordering_fields = ('id', 'user', 'course', 'enroll_date')
    search_fields = ('id', 'user', 'course', 'enroll_date', 'is_finished')
