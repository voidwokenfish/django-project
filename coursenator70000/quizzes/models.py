from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Quiz(models.Model):
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
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
    question = models.TextField()

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Вопрос квиза"
        verbose_name_plural = "Вопросы квиза"

class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    answer = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = "Ответ квиза"
        verbose_name_plural = "Ответы квиза"