import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from loguru import logger
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from server.api.core.pagination.base import StandardPagePagination
from server.api.v1.courses.permissions import IsAdminOrReadOnly
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


class LessonFilter(django_filters.FilterSet):
    """Фильтр для просмотра всех уроков одного модуля для вьюсета урока"""

    module = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Lesson
        fields = ['module']


class LessonViewSet(viewsets.ModelViewSet):
    """Вьюсет для CRUD операций над моделью урока"""

    queryset = Lesson.objects.filter().order_by('title')
    serializer_class = LessonListSerializer
    permission_classes = (IsAdminOrReadOnly,)
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


class ModuleFilter(django_filters.FilterSet):
    """Фильтр для вьюсета модуля"""

    course = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Module
        fields = ['course']


class ModuleViewSet(viewsets.ModelViewSet):
    """Вьюсет для CRUD операция над моделью модуля"""

    queryset = Module.objects.filter().order_by('title')
    serializer_class = ModuleListSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = StandardPagePagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_class = ModuleFilter
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
    permission_classes = (IsAdminOrReadOnly,)
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

    @action(detail=True, methods=['get'], url_path='content')
    def course_content(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)
            modules = course.modules.all()

            if request.user.is_authenticated:
                enrollments = Enrollment.objects.filter(course=course, user=request.user)
            else:
                enrollments = Enrollment.objects.none()

            return Response({
                "course": CourseDetailSerializer(course).data,
                "modules": ModuleListSerializer(modules, many=True).data,
                "enrollments": EnrollmentSerializer(enrollments, many=True).data
            })

        except Exception as e:
            logger.info(f"Ошибка {e}")


class EnrollmentViewSet(viewsets.ModelViewSet):
    """Вьюсет для CRUD операций над моделью зачислений"""

    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = StandardPagePagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    ordering_fields = ('id', 'user', 'course', 'enroll_date')
    search_fields = ('id', 'user', 'course', 'enroll_date', 'is_finished')
