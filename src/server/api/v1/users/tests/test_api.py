import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


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
def register_data(db, user):
    pass