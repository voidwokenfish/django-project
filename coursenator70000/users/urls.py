from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from .views import profile, register, user_login, send_reset_password_email

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/<str:username>/', profile, name='profile'),
    path('reset/<int:user_id>', send_reset_password_email, name='send_reset_password_email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)