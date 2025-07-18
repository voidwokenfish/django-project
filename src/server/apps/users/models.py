from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static
from Tools.i18n.pygettext import default_keywords


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, verbose_name="Никнейм")
    email = models.EmailField(unique=True, verbose_name="Эл. Почта")
    first_name = models.CharField(max_length=50, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=50, blank=True, verbose_name="Фамилия")
    is_active = models.BooleanField(default=False, verbose_name="Активен")
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return static('images/defaultpfp.jpg')

    def __str__(self):
        return f"Профиль {self.user.username}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
