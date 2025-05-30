from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (CourseUpdateView, complete_lesson, course_detail,
                    enroll_student, httptest, index, lesson_detail,
                    module_detail)

urlpatterns = [
    path('', index, name='index'),
    path('page/<int:page_number>', index, name='paginator'),
    path('topic/<int:topic_id>', index, name='topic'),
    path('course/<int:pk>', course_detail, name='course_detail'),
    path('course/<int:pk>/update', CourseUpdateView.as_view(), name='course_update'),
    path('course/module/<int:pk>', module_detail, name='module_detail'),
    path('course/module/lesson/<int:pk>', lesson_detail, name='lesson_detail'),
    path('test', httptest, name='httptest'),
    path('course/<int:pk>/enroll', enroll_student, name='enroll_student'),
    path('course/module/lesson/<int:pk>/complete', complete_lesson, name='complete_lesson'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)