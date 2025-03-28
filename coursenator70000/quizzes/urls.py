from django.urls import path
from .views import quiz_detail

urlpatterns = [
    path('quiz/<int:pk>/', quiz_detail, name='quiz_detail'),
]