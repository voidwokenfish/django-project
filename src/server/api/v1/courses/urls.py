from rest_framework.routers import DefaultRouter
from server.api.v1.courses.views import CourseViewSet


router = DefaultRouter()
router.register('courses', CourseViewSet, basename='courses')
