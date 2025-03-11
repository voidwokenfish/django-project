from django.urls import path
from .views import index, course_detail, CourseUpdateView


urlpatterns = [
    path('', index, name='index'),
    path('course/<int:pk>', course_detail, name='course_details'),
    path('course/<int:pk>/update', CourseUpdateView.as_view(), name='course_update'),
]