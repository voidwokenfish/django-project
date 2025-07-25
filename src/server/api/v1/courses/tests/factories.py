import factory

from datetime import date
from server.api.v1.users.tests.factories import UserFactory
from server.apps.courses.models import (Course, Enrollment, Lesson, Module,
                                        UserLessonCompleted)


class CourseFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания тестового курса"""

    class Meta:
        model = Course

    title = factory.Sequence(lambda n: f"Тестовый курс{n}")
    description = "Тестовое описание"
    price = 99
    is_linear = True
    is_active = True


class ModuleFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания тестового модуля, связанного с курсом"""

    class Meta:
        model = Module

    course = factory.SubFactory(CourseFactory)
    title = factory.Sequence(lambda n: f"Тестовый модуль{n}")
    number = factory.Sequence(lambda n: n)


class LessonFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания тестового урока, связанного с модулем"""

    class Meta:
        model = Lesson

    module = factory.SubFactory(ModuleFactory)
    title = factory.Sequence(lambda n: f"Тестовый урок{n}")


class EnrollmentFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания тестового зачисления,
     связанного с пользователем и курсом"""

    class Meta:
        model = Enrollment

    user = factory.SubFactory(UserFactory)
    course = factory.SubFactory(CourseFactory)
    enroll_date = date.today()
