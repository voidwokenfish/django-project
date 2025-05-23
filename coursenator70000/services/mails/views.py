from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.http import HttpResponse


User = get_user_model()

def register_confirm(request, uid, token):
    """Функция декодирует данные и завершает регистрацию"""
    uid_decoded = urlsafe_base64_decode(uid).decode()
    user = User.objects.get(pk=uid_decoded) #это я получаю пользователя шоб узнать хто это

    if user is not None and default_token_generator.check_token(user, token):
        #.check_token сравниваеит данные user и token(там тоже данные user но в токен обернутые)
        return HttpResponse("Регистрация прошла успешно!")

    else:
        return HttpResponse("Произошла ошибка.")

def email_confirm(request, uid, token):
    """Функция декодирует данные полученные от """
    uid_decoded = urlsafe_base64_decode(uid).decode()
    user = User.objects.get(pk=uid_decoded)  # это я получаю пользователя шоб узнать хто это

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Активация аккаунта прошла успешно!")
    else:
        return HttpResponse("Произошла ошибка.")




def reset_password(request, uid, token):
    """Функция декодирует данные и перенаправляет пользователя на страницу смены пароля"""
    uid_decoded = urlsafe_base64_decode(uid).decode()
    user = User.objects.get(pk=uid_decoded)

    if user is not None and default_token_generator.check_token(user, token):
        return HttpResponse("")
    else:
        return HttpResponse("")