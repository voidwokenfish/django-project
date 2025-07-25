from rest_framework.routers import DefaultRouter

from server.api.v1.news.views import NewsViewSet

router = DefaultRouter()

router.register('news', NewsViewSet, basename='news')