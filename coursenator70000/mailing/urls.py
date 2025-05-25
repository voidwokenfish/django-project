from django.urls import path
from .views import subscribe_email, register_confirm, reset_password, email_confirm

urlpatterns = [
    path('subscribe/', subscribe_email, name='subscribe_email'),
    path('registerconfirm/<uid>/<token>/', register_confirm, name='register_confirm' ),
    path('resetpassword/<uid>/<token>/', reset_password, name='reset_password'),
    path('emailconfirm/<uid>/<token>/', email_confirm, name='email_confirm'),
]