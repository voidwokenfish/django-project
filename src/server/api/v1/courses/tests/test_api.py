import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from server.api.v1.courses.serializers import CourseDetailSerializer, ModuleDetailSerializer, EnrollmentSerializer, \
    ModuleListSerializer
from server.api.v1.courses.tests.factories import (CourseFactory,
                                                   LessonFactory,
                                                   ModuleFactory, EnrollmentFactory)


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
    course = CourseFactory()
    modules = [ModuleFactory(course=course) for _ in range(3)]
    enrollments = [EnrollmentFactory(course=course, user=user) for _ in range(2)]

    return {
        "user": user,
        "course": course,
        "modules": modules,
        "enrollments": enrollments,
    }

def test_get_course_content(auth_client, course_data):
    course = course_data["course"]

    response = auth_client.get(f"/api/v1/courses/{course.id}/content/")

    expected_course_data = CourseDetailSerializer(
        course_data["course"]
    ).data
    expected_module_data = ModuleListSerializer(
        course_data["modules"], many=True
    ).data
    expected_enrollment_data = EnrollmentSerializer(
        course_data["enrollments"], many=True
    ).data

    assert response.status_code == 200
    assert response.data["course"] == expected_course_data
    assert response.data["modules"] == expected_module_data
    assert response.data["enrollments"] == expected_enrollment_data