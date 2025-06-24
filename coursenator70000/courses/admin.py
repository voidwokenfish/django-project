from django.contrib import admin
from quizzes.models import Quiz, QuizQuestion, QuizAnswer
from courses import help_texts
from courses.help_texts import COURSE_HELP_TEXT

from nested_admin.nested import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from .models import (Course, Enrollment, Lesson, Module, Topic,
                     UserLessonCompleted)


class QuizAnswerInline(NestedTabularInline):
    model = QuizAnswer
    extra = 1
    ordering = ('id',)
    inlines = []
    help_texts = None
    # fieldsets = ()


class QuizQuestionInline(NestedStackedInline):
    model = QuizQuestion
    extra = 1
    ordering = ('id',)
    inlines = [QuizAnswerInline]
    help_texts = None
    # fieldsets = ()


class QuizInline(NestedStackedInline):
    model = Quiz
    extra = 0
    ordering = ('id',)
    inlines = [QuizQuestionInline]
    help_texts = None
    # fieldsets = ()

class LessonInline(NestedStackedInline):
    model = Lesson
    extra = 0
    ordering = ('id',)
    inlines = []
    help_texts = None
    # fieldsets = ()

class ModuleInline(NestedStackedInline):
    model = Module
    extra = 0
    ordering = ('id',)
    inlines = [LessonInline, QuizInline]
    help_texts = help_texts.MODULE_HELP_TEXTS
    # fieldsets = ()

    def get_formset(self, request, obj, **kwargs):
        texts = self.help_texts
        kwargs.update(
            {"help_texts": texts},
        )
        return super().get_formset(request, obj, **kwargs)


@admin.register(Course)
class CourseAdmin(NestedModelAdmin):
    search_fields = ['title']
    search_help_text = "Поиск по названию"
    list_display = ("title", "price", "modules", "enrolled", "finished")
    help_texts = None
    inlines = [ModuleInline]
    fieldsets = (
        (
            None,
            {
                "fields": ("title", "description", "image", "is_linear", "topics",),
                "description": COURSE_HELP_TEXT,
            }
        ),
        (
            "Цена",
            {
                "fields": ("price",)
            }
        ),
    )

    def enrolled(self, obj):
        return obj.enrollments.count()

    def finished(self, obj): #obj - это сам объект - т.е. в данном случае один курс!
        return obj.enrollments.filter(is_finished=True).count()

    def modules(self, obj):
        return obj.modules.count()

    enrolled.short_description = "Зачислены"
    finished.short_description = "Окончили"
    modules.short_description = "Модули"

    # def response_add(self, request, obj, post_url_continue=None):
    #     pass
    #
    # def response_change(self, request, obj):
    #     pass
    #
    # def _is_valid(self, request, obj):
    #     pass




@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(UserLessonCompleted)
class UserLessonCompletedAdmin(admin.ModelAdmin):
    pass
