from datetime import timezone

import django_filters
from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from loguru import logger
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from server.api.core.pagination.base import StandardPagePagination
from server.api.v1.courses.permissions import IsAdminOrReadOnly
from server.api.v1.courses.serializers import (
    CourseDetailSerializer, CourseListSerializer, CourseWriteSerializer,
    EnrollmentSerializer, LessonDetailSerializer, LessonListSerializer,
    LessonWriteSerializer, ModuleContentItemSerializer, ModuleDetailSerializer,
    ModuleDetailWithProgressSerializer, ModuleListSerializer,
    ModuleWriteSerializer)
from server.api.v1.quizzes.serializers import QuizListSerializer, QuizDetailSerializer
from server.apps.courses.models import (Course, Enrollment, Lesson, Module,
                                        UserLessonCompleted)
from server.apps.quizzes.models import QuizAttempt
from server.apps.transactions.models import Transaction
from server.services.payments.payment import PaymentService


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

@action(detail=True, methods=['post'], url_path='complete')
def complete_lesson(self, request, pk=None):
    """"""

    try:
        lesson = self.get_object()
        obj = UserLessonCompleted.objects.get_or_create(
            lesson=lesson,
            user=request.user,
            completed_datetime = timezone.now().date()
        )

        return Response({
            "status" : "completed"
        })
    except Exception as e:
        logger.info(f"Ошибка {e}")
        return Response({
            "status" : "error"
        })


class ModuleFilter(django_filters.FilterSet):
    """Фильтр для вьюсета модуля"""

    course = django_filters.CharFilter(lookup_expr='icontains')
    course_id = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Module
        fields = ['course', 'course_id']


class ModuleViewSet(viewsets.ModelViewSet):
    """Вьюсет для CRUD операций над моделью модуля курса
     с дополнительным экшеном для получения содержимого модуля с прогрессом."""

    queryset = Module.objects.filter().order_by('title')
    serializer_class = ModuleListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = StandardPagePagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filterset_class = ModuleFilter
    ordering_fields = ('id', 'title', 'course')
    search_fields = ('id', 'title')

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора в зависимости от действия вьюсета
        """

        if self.action in ("create", "update", "partial_update"):
            return ModuleWriteSerializer
        if self.action == "retrieve":
            return ModuleDetailSerializer
        return self.serializer_class

    @action(detail=True, methods=['get'], url_path='content')
    def module_content(self, request, pk=None):
        """
        Дополнительный метод (action), возвращающий содержимое модуля курса:
        список уроков и квизов с флагом разблокировки,
        списки завершённых уроков и квизов пользователя,
        процент прогресса прохождения модуля.
        """

        try:

            module = self.get_object()
            course = module.course

            lessons = list(module.lessons.all())
            quizzes = list(module.quizzes.all())

            items = sorted(
                [{"type": "lesson", "obj": LessonDetailSerializer(lesson).data} for lesson in lessons] +
                [{"type": "quiz", "obj": QuizDetailSerializer(quiz).data} for quiz in quizzes],
                key=lambda x: x["obj"]["course_order"]
            )

            completed_lessons = self._get_completed_lessons(lessons)

            completed_quizzes = self._get_completed_quizzes(quizzes)

            content_items = self._set_unlock_flags(
                course=course,
                items=items,
                completed_lessons=completed_lessons,
                completed_quizzes=completed_quizzes,
            )

            progressbar = round(
                (len(completed_lessons) + len(completed_quizzes)) / len(content_items) * 100
            )
            data = {
                "module": module,
                "content_items": content_items,
                "completed_lessons": list(completed_lessons),
                "completed_quizzes": list(completed_quizzes),
                "progressbar": progressbar
            }
            serializer = ModuleDetailWithProgressSerializer(instance=data)

            return Response(serializer.data, status=200)

        except Exception as e:
            logger.info(f'Ошибка {e}')
            return Response()

    def _get_completed_lessons(self, lessons):
        """
        Возвращает список ID уроков из переданного списка, которые текущий пользователь уже прошёл.
        """
        objs = UserLessonCompleted.objects.filter(
            user = self.request.user, lesson__in=lessons
        ).values_list('lesson_id', flat=True)
        return objs

    def _get_completed_quizzes(self, quizzes) -> set:
        """
        Возвращает список id квизов, которые пользователь прошёл успешно,
        то есть у которых максимальный набранный балл пользователя >= проходного балла.
        Если пользователь не аутентифицирован или список квизов пуст — возвращает пустое множество.
        """

        user = self.request.user

        if not user.is_authenticated or not quizzes:
            return set()

        quiz_ids = [quiz.id for quiz in quizzes]

        max_scores = (
            QuizAttempt.objects.filter(user=user, quiz__in=quiz_ids)
            .values('quiz')
            .annotate(max_score=Max('score'))
        )

        user_scores = {item['quiz']: item['max_score'] for item in max_scores}

        completed_quiz_ids = {
            quiz.id for quiz in quizzes
            if user_scores.get(quiz.id, 0) >= quiz.pass_score
        }

        return completed_quiz_ids

    def _set_unlock_flags(self, course, items, completed_lessons, completed_quizzes):
        """
        Устанавливает для каждого элемента (урока или квиза) флаг `is_unlocked` в зависимости от
        настроек курса (линейный или нет) и статуса прохождения предыдущих элементов.

        В линейном курсе следующий элемент разблокируется только если предыдущий завершён.
        """

        unlocked = True  # первый элемент всегда доступенн
        for item in items:
            if not course.is_linear:
                item["is_unlocked"] = True
                continue

            if unlocked:
                item["is_unlocked"] = True
            else:
                item["is_unlocked"] = False

            # Прверяем, завершен ли текущий элемент
            if item["type"] == "lesson" and item["obj"]["id"] in completed_lessons:
                unlocked = True
            elif item["type"] == "quiz" and item["obj"]["id"] in completed_quizzes:
                unlocked = True
            else:
                unlocked = False  # блокируем следующий, если текущий не завершен

        return items



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
        """Выбирает подходящий сериализатор в зависимости от выполняемого действия"""

        if self.action in ('create', 'update', 'partial_update',):
            return CourseWriteSerializer
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return self.serializer_class

    @action(detail=True, methods=['get'], url_path='content')
    def course_content(self, request, pk=None):
        """
        Возвращает подробную информацию о курсе,
        его модулях и текущих зачислениях пользователя (если он авторизован).
        """

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


    @action(detail=True, methods=['post'], url_path='enroll')
    def enroll(self, request, pk=None):
        """
        Создаёт запись о платёжной транзакции для оплаты курса текущим пользователем
        и возвращает ссылку для проведения платежа.
        """
        user = request.user
        course = self.get_object()
        description = f'Оплата курса {course.title}'
        transaction = Transaction.objects.create(
            user=user,
            course=course,
            amount=course.price,
            description=description
        )
        url = PaymentService(transaction).execute()

        return Response({
            "payment_url" : url
        })


class EnrollmentViewSet(viewsets.ModelViewSet):
    """Вьюсет для CRUD операций над моделью зачислений"""

    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = StandardPagePagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    ordering_fields = ('id', 'user', 'course', 'enroll_date')
    search_fields = ('id', 'user', 'course', 'enroll_date', 'is_finished')
