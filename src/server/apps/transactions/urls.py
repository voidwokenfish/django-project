from django.urls import path
from server.apps.transactions.views import YookassaWebHookView

urlpatterns = [
    path('notifications', YookassaWebHookView.as_view(), name='notifications'),
]