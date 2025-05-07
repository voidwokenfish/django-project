from django.urls import path
from .views import subscribe_email

urlpatterns = [
    path('subscribe/', subscribe_email, name='subscribe_email'),
]