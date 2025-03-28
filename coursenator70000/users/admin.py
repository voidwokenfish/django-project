from django.contrib import admin

from .models import User, UserLessonCompleted, UserQuizAttempt


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(UserLessonCompleted)
class UserLessonCompletedAdmin(admin.ModelAdmin):
    pass

@admin.register(UserQuizAttempt)
class UserQuizAttemptAdmin(admin.ModelAdmin):
    pass
