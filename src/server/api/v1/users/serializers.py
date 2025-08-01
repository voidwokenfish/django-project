from django.contrib.auth import get_user_model
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
    username = serializers.CharField(max_length=50, required=True, unique=True)
    email = serializers.EmailField(required=True, unique=True)
    password = serializers.CharField(required=True, min_length=8, max_length=128, write_only=True)
    confirm_password = serializers.CharField(required=True, min_length=8, max_length=128, write_only=True)


    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Почта уже зарегистрирована.')
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким юзернеймом уже существует.")
        return value

    def validate(self, data):
        """Пароль"""

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("")
        return data

    def create(self, validated_data):

        validated_data["confirm_password"].pop()
        user = User.objects.create_user(**validated_data)
        return user
