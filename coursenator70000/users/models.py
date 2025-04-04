from django.contrib.auth.models import AbstractUser
from django.db import models


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

class UserLessonCompleted(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey('courses.Lesson', on_delete=models.CASCADE)
    completed_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student, self.lesson, self.completed_datetime

    class Meta:
        verbose_name = "Завершенный урок"
        verbose_name_plural = "Завершенные уроки"

class UserQuizAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey('quizzes.Quiz', on_delete=models.CASCADE)
    attempt_datetime = models.DateTimeField()
    score = models.IntegerField()

    def __str__(self):
        return f"Student: {self.student}, Quiz: {self.quiz}, Date: {self.attempt_datetime}, Score: {self.score}"

    class Meta:
        verbose_name = "Попытка выполнить квиз"
        verbose_name_plural = "Попытки выполнить квизы"