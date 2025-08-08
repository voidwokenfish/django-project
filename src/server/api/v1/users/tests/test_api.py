import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient


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
def valid_register_data(db):
    """Фикстура с валидными данными для регистрации пользователя."""
    return {
        "username": "goblinking",
        "email": "ofthe@test.test",
        "password": "Darkstormgalaxy123",
        "confirm_password": "Darkstormgalaxy123",
    }

@pytest.fixture()
def invalid_register_data(db):
    """Фикстура с невалидными данными для регистрации."""
    return {
        "username": "showme",
        "email": "thechampion@test.test",
        "password": "OfLight123",
        "confirm_password": "Illshowyoutheheraldofdarkness",
    }
def test_register_success(auth_client, valid_register_data):

    response = auth_client.post('/api/v1/register/', data=valid_register_data, format='json')

    assert response.status_code == status.HTTP_201_CREATED


def test_register_failure(auth_client, invalid_register_data):

    response = auth_client.post('/api/v1/register/', data=invalid_register_data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
