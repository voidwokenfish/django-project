from django.urls import path

from .views import get_answer, get_finish, get_questions, quiz_detail

urlpatterns = [
    path('quiz/<int:pk>/', quiz_detail, name='quiz_detail'),
    path('get-questions/start', get_questions, {'is_start': True}, name='get-questions'),
    path('get-questions', get_questions, {'is_start': False}, name='get-questions'),
    path('get-answer', get_answer, name='get-answer'),
    path('get-finish', get_finish, name='get-finish'),
]