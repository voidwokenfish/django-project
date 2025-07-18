from rest_framework import serializers

from server.apps.users.models import Profile, User


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
