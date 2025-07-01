from django.urls import path

from .views import (email_confirm, register_confirm, reset_password,
                    subscribe_email)

app_name = 'mailing'

urlpatterns = [
    path('subscribe/', subscribe_email, name='subscribe_email'),
    path('registerconfirm/<uid>/<token>/', register_confirm, name='register_confirm'),
    path('resetpassword/<uid>/<token>/', reset_password, name='reset_password'),
    path('emailconfirm/<uid>/<token>/', email_confirm, name='email_confirm'),
]