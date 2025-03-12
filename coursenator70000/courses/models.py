from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='courses_images/', null=True, blank=True, default='default.jpg')
    is_linear = models.BooleanField() # Нужно ли студенту на данном курсе завершать урок, чтобы перейти к следующему

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    number = models.IntegerField() # Номер модуля в курсе

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.TextField()
    number = models.IntegerField()
    video_url = models.URLField()
    lesson_details = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Topic(models.Model):
    title = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to="topics")
    is_active = models.BooleanField() # Досупен ли курс, мб на переработке

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enroll_date = models.DateField()

    def __str__(self):
        return f"{self.course.title}, {self.user.email}"

    class Meta:
        verbose_name = "Зачисление"
        verbose_name_plural = "Зачисления"