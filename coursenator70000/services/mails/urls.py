from django.urls import path, include

from views import register_confirm, reset_password, email_confirm

urlpatterns = [
    path('registerconfirm/<uid>/<token>/', register_confirm, name='register_confirm' ),
    path('resetpassword/<uid>/<token>', reset_password, name='reset_password'),
    path('emailconfirm/<uid>/<token>', email_confirm, name='email_confirm'),
]