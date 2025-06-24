from django.urls import path
from transactions.views import YookassaWebHookView

urlpatterns = [
    path('notifications', YookassaWebHookView.as_view(), name='notifications'),
]