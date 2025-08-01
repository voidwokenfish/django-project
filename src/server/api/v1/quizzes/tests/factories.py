from datetime import date

import factory

from server.api.v1.courses.tests.factories import ModuleFactory
from server.api.v1.users.tests.factories import UserFactory
from server.apps.quizzes.models import (Quiz, QuizAnswer, QuizAttempt,
                                        QuizQuestion)


class QuizFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания тестового квиза, связанного с модулем"""

    class Meta:
        model = Quiz

    module = factory.SubFactory(ModuleFactory)
    title = "Тестовый квиз"
    number = 1
    course_order = factory.Sequence(lambda n: n+1)
    pass_score = 60


class QuizQuestionFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания вопроса связанного с квизом."""

    class Meta:
        model = QuizQuestion

    quiz = factory.SubFactory(QuizFactory)
    text = factory.Sequence(lambda n: f"Вопрос{n}")


class QuizAnswerFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания ответа, связанного с вопросом."""

    class Meta:
        model = QuizAnswer

    text = factory.Sequence(lambda n: f"Ответ {n}")
    question = factory.SubFactory(QuizQuestionFactory)
    is_correct = False

class QuizAttemptFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания попытки квиза после его завершения"""

    class Meta:
        model = QuizAttempt

    user = factory.SubFactory(UserFactory)
    quiz = factory.SubFactory(QuizFactory)
    date = date.today()
    score = 60