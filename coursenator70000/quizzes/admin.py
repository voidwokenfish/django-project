from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Quiz, QuizQuestion, QuizAnswer, QuizAttempt


@admin.action(description="Декомплитрекваенатор")
def deactivate_complete_req_field(modeladmin, request, queryset):
    queryset.update(is_complete_required=False)

class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 0

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ["title", "number", "total_quiz_questions", "display_course", "course_order", "first_quiz", "pass_score", "is_complete_required"]
    list_editable = ["number", "course_order", "pass_score", "is_complete_required"]
    search_fields = ["title"]
    inlines = [QuizQuestionInline]
    actions = [deactivate_complete_req_field]

    def first_quiz(self, obj):
        return obj.course_order == 2

    first_quiz.short_description = "Первяк"
    first_quiz.boolean = True

    def total_quiz_questions(self, obj):
        return QuizQuestion.objects.filter(quiz=obj).count()

    total_quiz_questions.short_description = "Кол-во вопросов"

    def display_course(self, obj):
        link = reverse("admin:courses_course_change", args=[obj.course.id])
        return format_html('<a href="{}">{}</a>', link, obj.course)

    display_course.short_description = "Курс!"


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    pass

