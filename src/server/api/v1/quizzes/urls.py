from rest_framework.routers import DefaultRouter

from server.api.v1.quizzes.views import QuizViewSet

router = DefaultRouter()
router.register('quizzes', QuizViewSet, basename='quizzes')