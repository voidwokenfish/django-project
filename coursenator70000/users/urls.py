from django.contrib.auth.views import LogoutView
from django.urls import path, include

from .views import register, user_login
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]