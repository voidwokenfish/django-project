from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Module


User = get_user_model()


class Quiz(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=300)
    number = models.IntegerField()
    course_order = models.IntegerField(default=0)
    pass_score = models.IntegerField()
    is_complete_required = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Квиз"
        verbose_name_plural = "Квизы"

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Вопрос квиза"
        verbose_name_plural = "Вопросы квиза"

class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Ответ квиза"
        verbose_name_plural = "Ответы квиза"

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    score = models.IntegerField()

    def __str__(self):
        return f"Student: {self.user}, Quiz: {self.quiz}, Date: {self.date}, Score: {self.score}"

    class Meta:
        verbose_name = "Попытка выполнить квиз"
        verbose_name_plural = "Попытки выполнить квизы"