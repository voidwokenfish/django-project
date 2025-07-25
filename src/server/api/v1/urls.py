from django.urls import include, path

from server.api.v1.courses.urls import router as courses_router
from server.api.v1.news.urls import router as news_router
from server.api.v1.quizzes.urls import router as quizzes_router
from server.api.v1.users.urls import router as users_router

urlpatterns = [
    path('', include(courses_router.urls)),
    path('', include(users_router.urls)),
    path('', include(quizzes_router.urls)),
    path('', include(news_router.urls)),
]
