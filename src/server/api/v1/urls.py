from django.urls import include, path
from server.api.v1.courses.urls import router as courses_router


urlpatterns = [
    path('', include(courses_router.urls))
]