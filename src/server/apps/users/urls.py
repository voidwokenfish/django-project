from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (profile, register, reset_email_form_view,
                    reset_password_form_view, reset_password_with_email,
                    send_change_email_email, send_reset_password_email,
                    user_login)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/<str:username>/', profile, name='profile'),
    path('reset/<data>/', send_reset_password_email, name='send_reset_password_email'),
    path('resetm/<data>/', send_change_email_email, name='send_change_email_email'),
    path('login/forgotpassword/', reset_password_with_email, name='reset_password_with_email'),
    path('changepassword/<int:user_id>/', reset_password_form_view, name='reset_password_form_view'),
    path('changeemail/<int:user_id>/', reset_email_form_view, name='reset_email_form_view'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)