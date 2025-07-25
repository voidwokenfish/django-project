import factory

from server.apps.users.models import Profile, User


class UserFactory(factory.django.DjangoModelFactory):
    """Фабрика для создания тестового пользователя"""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'Пользователь{n}')
    email = factory.Sequence(lambda n: f'testemail{n}@test.test')
    password = factory.Sequence(lambda n: f'<PASSWORD>{n}')
    is_active = True

