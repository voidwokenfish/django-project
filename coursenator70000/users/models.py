from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ManyToManyField

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, verbose_name="Никнейм")
    email = models.EmailField(unique=True, verbose_name="Эл. Почта")
    first_name = models.CharField(max_length=50, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=50, blank=True, verbose_name="Фамилия")
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



