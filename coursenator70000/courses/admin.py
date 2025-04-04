from django.contrib import admin
from .models import Course, Module, Lesson, Enrollment, Topic, UserLessonCompleted

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    pass

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass

@admin.register(UserLessonCompleted)
class UserLessonCompletedAdmin(admin.ModelAdmin):
    pass
