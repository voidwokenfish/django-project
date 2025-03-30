from django.contrib import admin

from .models import User, UserLessonCompleted, UserQuizAttempt


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "first_name", "last_name", "is_superuser", "is_staff"]


@admin.register(UserLessonCompleted) #todo Перенос куда надо
class UserLessonCompletedAdmin(admin.ModelAdmin):
    pass

@admin.register(UserQuizAttempt)
class UserQuizAttemptAdmin(admin.ModelAdmin):
    pass
