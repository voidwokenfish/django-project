from django.urls import path
from .views import index, course_detail, CourseUpdateView, module_detail, lesson_detail, httptest, enroll_student
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('course/<int:pk>', course_detail, name='course_detail'),
    path('course/<int:pk>/update', CourseUpdateView.as_view(), name='course_update'),
    path('course/module/<int:pk>', module_detail, name='module_detail'),
    path('course/module/lesson/<int:pk>', lesson_detail, name='lesson_detail'),
    path('test', httptest, name='httptest'),
    path('course/<int:pk>/enroll', enroll_student, name='enroll_student'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)