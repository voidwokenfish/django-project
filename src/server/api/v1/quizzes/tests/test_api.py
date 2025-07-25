import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from server.api.v1.quizzes.tests.factories import (QuizAnswerFactory,
                                                   QuizAttemptFactory,
                                                   QuizQuestionFactory)
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

@pytest.fixture
def quiz_data(db):
    """Тестовый квиз с 2мя вопросом и 2мя ответами на первый вопрос"""

    question = QuizQuestionFactory(text="MILK + CUCUMBER?")
    correct = QuizAnswerFactory(question=question, text="YES!", is_correct=True)
    wrong = QuizAnswerFactory(question=question, text="No...", is_correct=False)
    next_question = QuizQuestionFactory(quiz=question.quiz)

    return {
        "quiz": question.quiz,
        "question": question,
        "correct": correct,
        "wrong": wrong,
        "next_question": next_question,
    }

def test_quiz_start(auth_client, quiz_data):
    """Тест квиза на возврат первого вопроса"""

    quiz_id = quiz_data["quiz"].id
    response = auth_client.get(f"/api/v1/quizzes/{quiz_id}/start/")
    assert response.status_code == 200
    assert response.data["text"] == "MILK + CUCUMBER?"

def test_quiz_answer_correct(auth_client, quiz_data):
    """Тест квиза на правильность ответа"""

    quiz = quiz_data["quiz"]
    question = quiz_data["question"]
    correct = quiz_data["correct"]

    response = auth_client.post(f"/api/v1/quizzes/{quiz.id}/answer/",{
        "question": question.id,
        "answer": correct.id
    })

    assert response.status_code == 200
    assert response.data["correct"] is True

def test_quiz_answer_wrong(auth_client, quiz_data):
    """Тест квиза на неправильность ответа"""

    quiz = quiz_data["quiz"]
    question = quiz_data["question"]
    wrong = quiz_data["wrong"]

    response = auth_client.post(f"/api/v1/quizzes/{quiz.id}/answer/",{
        "question": question.id,
        "answer": wrong.id
    })

    assert response.status_code == 200
    assert response.data["correct"] is False

def test_quiz_next_question_found(auth_client, quiz_data):
    """Тест квиза на возврат следующего вопроса0"""

    quiz = quiz_data["quiz"]
    question = quiz_data["question"]
    next_question = quiz_data["next_question"]

    response = auth_client.post(f"/api/v1/quizzes/{quiz.id}/next/",{
        "question": question.id,
        "quiz": quiz.id
    })

    assert response.status_code == 200
    assert response.data["id"] == next_question.id
    assert response.data["text"] == next_question.text

def test_quiz_next_question_not_found(auth_client, quiz_data):
    """Тест квиза на возврат отсутсвия следующего вопроса"""

    quiz = quiz_data["quiz"]
    last_question = quiz_data["next_question"]

    response = auth_client.post(f"/api/v1/quizzes/{quiz.id}/next/",{
        "question": last_question.id,
        "quiz": quiz.id
    })

    assert response.status_code == 404
    assert response.data['flag'] == "quiz_finished"

def test_quiz_finish(auth_client, quiz_data, user):
    """
    Тест квиза на возврат результатов теста
     и создания/обновления записи о попытке
     """

    quiz = quiz_data["quiz"]
    user = user

    score = 100

    response = auth_client.post(f"/api/v1/quizzes/{quiz.id}/finish/",{
        "user": user.id,
        "quiz": quiz.id,
        "score": int(score)
    })

    assert response.status_code == 200
    assert response.data["score"]
    assert response.data["percent"]

    attempt = QuizAttempt.objects.filter(quiz=quiz, user=user).first()
    assert attempt is not None
    assert attempt.score == score

def test_quiz_attempt_update(auth_client, quiz_data, user):

    quiz = quiz_data["quiz"]
    user = user

    old_attempt = QuizAttemptFactory(score=50)
    new_score = 100

    response = auth_client.post(f"/api/v1/quizzes/{quiz.id}/finish/",{
        "user": user.id,
        "quiz": quiz.id,
        "score": int(new_score)
    })

    assert response.status_code == 200

    attempt = QuizAttempt.objects.get(user=user, quiz=quiz)
    assert attempt.score == new_score
