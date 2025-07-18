from rest_framework.routers import DefaultRouter

from server.api.v1.courses.views import (CourseViewSet, EnrollmentViewSet,
                                         LessonViewSet, ModuleViewSet)

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='courses')
router.register('modules', ModuleViewSet, basename='modules')
router.register('lessons', LessonViewSet, basename='lessons')
router.register('enrollments', EnrollmentViewSet, basename='enrollments')
