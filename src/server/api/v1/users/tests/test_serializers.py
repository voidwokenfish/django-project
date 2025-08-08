import pytest
from loguru import logger

from server.api.v1.users.serializers import RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_register_serializer_valid_data(test_log_data):

    data = {
        'username': 'NicolasCage',
        'email': 'IamTheBestActor@best.actor',
        'password': 'Cagebestactor123',
        'confirm_password': 'Cagebestactor123',
    }

    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid()

    user = serializer.save()

    assert user.username == data['username']
    assert user.check_password(data['password'])

@pytest.mark.django_db
def test_register_serializer_duplicate_email(test_log_data):
    data = {
        'username': 'NicolasCage',
        'email': 'IamTheBestActor@best.actor',
        'password': 'Cagebestactor123',
        'confirm_password': 'Cagebestactor123',
    }

    serializer = RegisterSerializer(data=data)
    is_valid = serializer.is_valid()
    serializer.save()
    serializer = RegisterSerializer(data=data)
    is_valid = serializer.is_valid()

    test_log_data['validation_errors'] = serializer.errors

    assert not is_valid

    assert "email" in serializer.errors


@pytest.mark.django_db
def test_register_serializer_missing_email(test_log_data):
    data = {
        'username': 'NicolasCage',
        'password': 'Cagebestactor123',
        'confirm_password': 'Cagebestactor123',
    }
    serializer = RegisterSerializer(data=data)
    is_valid = serializer.is_valid()

    test_log_data['validation_errors'] = serializer.errors

    assert not is_valid
    assert "email" in serializer.errors


@pytest.mark.django_db
def test_register_serializer_duplicate_username(test_log_data):
    data = {
        'username': 'NicolasCage',
        'email': 'IamTheBestActor@best.actor',
        'password': 'Cagebestactor123',
        'confirm_password': 'Cagebestactor123',
    }
    serializer = RegisterSerializer(data=data)
    is_valid = serializer.is_valid()
    serializer.save()
    serializer = RegisterSerializer(data=data)
    is_valid = serializer.is_valid()

    test_log_data['validation_errors'] = serializer.errors

    assert not is_valid

    assert "username" in serializer.errors

@pytest.mark.django_db
def test_register_serializer_missing_username(test_log_data):
    data = {
        'email': 'IamTheBestActor@best.actor',
        'password': 'Cagebestactor123',
        'confirm_password': 'Cagebestactor123',
    }

    serializer = RegisterSerializer(data=data)
    is_valid = serializer.is_valid()

    test_log_data['validation_errors'] = serializer.errors

    assert not is_valid
    assert "username" in serializer.errors

@pytest.mark.django_db
def test_register_serializer_missing_password(test_log_data):
    data = {
        'username': 'NicolasCage',
        'email': 'IamTheBestActor@best.actor',
    }

    serializer = RegisterSerializer(data=data)
    is_valid = serializer.is_valid()

    test_log_data['validation_errors'] = serializer.errors

    assert not is_valid
    assert "password" in serializer.errors

@pytest.mark.django_db
def test_register_serializer_bad_password(test_log_data):
    data = {
        'username': 'NicolasCage',
        'email': 'IamTheBestActor@best.actor',
        'password': 'cagebe',
        'confirm_password': 'cagebe',
    }

    serializer = RegisterSerializer(data=data)
    is_valid = serializer.is_valid()

    test_log_data['validation_errors'] = serializer.errors

    assert not is_valid
    assert "password" in serializer.errors

@pytest.mark.django_db
def test_register_serializer_missing_confirm_password(test_log_data):
    data = {
        'username': 'NicolasCage',
        'email': 'IamTheBestActor@best.actor',
        'password': 'Cagebestactor123',
    }

    serializer = RegisterSerializer(data=data)
    is_valid = serializer.is_valid()

    test_log_data['validation_errors'] = serializer.errors

    assert not is_valid
    assert "confirm_password" in serializer.errors

@pytest.mark.django_db
def test_register_serializer_bad_confirm_password(test_log_data):
    data = {
        'username': 'NicolasCage',
        'email': 'IamTheBestActor@best.actor',
        'password': 'Cagebestactor123',
        'confirm_password': 'cagebestctor123',
    }
    serializer = RegisterSerializer(data=data)
    is_valid = serializer.is_valid()

    test_log_data['validation_errors'] = serializer.errors

    assert not is_valid
    assert any("не совпадают" in str(err) for err in serializer.errors["non_field_errors"])

