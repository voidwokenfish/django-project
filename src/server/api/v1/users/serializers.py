from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from rest_framework import serializers

from server.apps.users.models import Profile

User = get_user_model()

class UserListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка пользователей"""

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'is_active'
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра одного пользователя"""

    class Meta:
        model = User
        fields = '__all__'


class UserWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения пользователя"""

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active']


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профилей"""

    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=8, max_length=128, write_only=True)
    confirm_password = serializers.CharField(required=True, min_length=8, max_length=128, write_only=True)


    def validate_email(self, value):
        """Проверяет, что email ещё не зарегистрирован.
         Если уже есть - вызывает ошибку."""

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Почта уже зарегистрирована.')
        return value

    def validate_username(self, value):
        """Проверяет, что имя пользователя уникально.
         Если пользователь с таким именем уже есть - вызывает ошибку."""

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким юзернеймом уже существует.")
        return value

    def validate_password(self, value):
        """Проверяет, что пароль содержит хотя бы одну цифру и одну заглавную букву.
         Если нет - вызывает ошибку."""

        if not any(c.isdigit() for c in value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну цифру.")
        if not any(c.isupper() for c in value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")
        return value

    def validate(self, data):
        """Проверяет, что пароль и подтверждение пароля совпадают.
         Если не совпадают - вызывает ошибку."""

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        """Создаёт нового пользователя после удаления поля подтверждения пароля.
         Используется после успешной валидации."""

        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get("username")
        password = int(data.get("password"))

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Неверные логин или паролью")

        data["user"] = user
        return data

