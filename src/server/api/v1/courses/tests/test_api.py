import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from server.api.v1.courses.serializers import (CourseDetailSerializer,
                                               EnrollmentSerializer,
                                               ModuleDetailSerializer,
                                               ModuleListSerializer)
from server.api.v1.courses.tests.factories import (CourseFactory,
                                                   EnrollmentFactory,
                                                   LessonFactory,
                                                   ModuleFactory)
from server.api.v1.quizzes.serializers import QuizDetailSerializer
from server.api.v1.quizzes.tests.factories import QuizFactory
from server.apps.courses.models import UserLessonCompleted
from server.apps.quizzes.models import QuizAttempt


User = get_user_model()


@pytest.fixture
def api_client():
    """Клиент, который отправляет http запросы в тестах"""

    return APIClient()

@pytest.fixture
def user(db):
    """Ф-я создает пользователя в тестовой базе"""

    return User.objects.create_user(
        username="testuser",
        password="testpword",
        email="testemail@test.test"
    )

@pytest.fixture
def auth_client(api_client, user):
    """Авторизация клиента через юзера без логина по токену"""

    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture()
def course_data(db, user):
    """Тестовые данные"""

    course = CourseFactory()
    module = ModuleFactory(course=course)

    lesson = LessonFactory(module=module)
    quiz = QuizFactory(module=module)
    quiz_not_completed = QuizFactory(module=module)

    UserLessonCompleted.objects.create(user=user, lesson=lesson)

    QuizAttempt.objects.create(user=user, quiz=quiz, score=80)
    QuizAttempt.objects.create(user=user, quiz=quiz_not_completed, score=30)


    enrollments = [EnrollmentFactory(course=course, user=user) for _ in range(2)]
    course2 = CourseFactory()
    modules2 = [ModuleFactory(course=course2) for _ in range(3)]

    return {
        "user": user,
        "course": course,
        "module": module,
        "lesson": lesson,
        "quiz": quiz,
        "quiz_not_completed": quiz_not_completed,
        "enrollments": enrollments,
        'course_no_enroll': course2,
        "modules2": modules2,
    }

def test_get_course_content(auth_client, course_data):
    """Тест course_content на возврат данных о курсе,
     его модулей и зачислений на него пользователем"""

    course = course_data["course"]

    response = auth_client.get(f"/api/v1/courses/{course.id}/content/")

    expected_course_data = CourseDetailSerializer(
        course_data["course"]
    ).data
    expected_module_data = ModuleListSerializer(
        [course_data["module"]], many=True
    ).data
    expected_enrollment_data = EnrollmentSerializer(
        course_data["enrollments"], many=True
    ).data

    assert response.status_code == 200
    assert response.data["course"] == expected_course_data
    assert response.data["modules"] == expected_module_data
    assert response.data["enrollments"] == expected_enrollment_data

def test_get_course_content_no_enrollments(auth_client, course_data):
    """Тест course_content на возврат пустого списка зачислений на курс,
     если их нет"""

    course = course_data["course_no_enroll"]

    response = auth_client.get(f"/api/v1/courses/{course.id}/content/")

    expected_course_data = CourseDetailSerializer(
        course_data["course_no_enroll"]
    ).data
    expected_module_data = ModuleListSerializer(
        course_data["modules2"], many=True
    ).data

    assert response.status_code == 200
    assert response.data["course"] == expected_course_data
    assert response.data["modules"] == expected_module_data
    assert response.data["enrollments"] == []

def test_get_module_content(auth_client, course_data):
    """
    Проверяет корректность ответа API при запросе контента модуля.

    Тест выполняет следующие проверки:
    - Статус ответа должен быть 200 OK.
    - Данные модуля в ответе совпадают с сериализованными данными модуля из тестовых данных.
    - В ответе присутствует список элементов контента (content_items) и он не пустой.
    - Каждый элемент content_items содержит обязательные ключи: 'type', 'obj', 'is_unlocked'.
    - В ответе есть списки completed_lessons и completed_quizzes, и они являются списками.
    - В списке completed_quizzes присутствует id пройденного квиза, а id непройденного квиза отсутствует.
    - Значение прогресс-бара находится в диапазоне от 0 до 100 включительно.
    """

    module = course_data["module"]
    course = course_data["course"]

    lessons = course_data["lesson"]

    expected_quiz_id = QuizDetailSerializer(course_data["quiz"]).data["id"]
    expected_quiz_not_completed_id = QuizDetailSerializer(course_data["quiz_not_completed"]).data["id"]

    expected_module = ModuleDetailSerializer(module).data

    response = auth_client.get(f"/api/v1/modules/{module.id}/content/")
    data = response.json()

    assert response.status_code == 200

    assert response.data["module"] == expected_module

    content_items = data["content_items"]
    assert isinstance(content_items, list)
    assert content_items
    item = content_items[0]
    assert "type" in item
    assert "obj" in item
    assert "is_unlocked" in item

    assert "completed_lessons" in data
    assert isinstance(data["completed_lessons"], list)
    assert "completed_quizzes" in data
    assert isinstance(data["completed_quizzes"], list)

    assert data["completed_quizzes"] == [expected_quiz_id]
    assert [expected_quiz_not_completed_id] not in data["completed_quizzes"]

    assert 0 <= data["progressbar"] <= 100

#todo Написать тест обрабатывающий отсутсвие данных в content_items и добавить в тестируемую ф-ю обработку этого