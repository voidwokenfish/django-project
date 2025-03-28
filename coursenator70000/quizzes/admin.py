from django.contrib import admin

from .models import Quiz, QuizQuestion, QuizAnswer


# Register your models here.
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    pass

