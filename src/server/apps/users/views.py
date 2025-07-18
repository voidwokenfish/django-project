from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse
from loguru import logger

from server.apps.courses.models import Enrollment
from server.apps.periodic_tasks.tasks import send_user_email
from server.services.mails.enums import MailTrigger

from .forms import (LoginForm, PasswordForgotForm, ProfileAvatarForm,
                    RegisterForm, SetNewEmailForm, SetNewPasswordForm)
from .models import Profile

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            send_user_email.delay(MailTrigger.REGISTER_CONFIRM.value, user.id)

            return redirect('login')

    else:
        form = RegisterForm() #При GET запросе

    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def profile(request, username):
    if request.user.username != username:
        return redirect('index')

    user = User.objects.get(username=username)
    profile = user.profile
    courses = []
    enrollments = Enrollment.objects.filter(user=user)

    for enrollment in enrollments:
        courses.append(enrollment.course)

    if request.method == 'POST':
        form = ProfileAvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile.save()
            return redirect('profile', username=user.username)
    else:
        form = ProfileAvatarForm(instance=request.user.profile)

    return render(request, 'profile.html', {
        "profile": profile,
        "user": user,
        "courses": courses,
        "enrollments": enrollments,
        "form": form
    })

def send_change_email_email(request, data: str):
    """Функция принимает в есбя id пользователя и создает задачу на отправку письма для смены почты"""
    try:
        user = user_checker(request, data)
        if user:
            send_user_email.delay(MailTrigger.MAIL_CONFIRM.value, user.id)
            messages.success(request, "Письмо для смены почты отправлено на вашу почту.")
            return HttpResponseRedirect(f"/profile/{user.username}")
        else:
            return HttpResponse("Пользователь с такими данными не найден. Повторите попытку.")
    except Exception as err:
        logger.error(err)
        return HttpResponse("Ошибка при отправке письма")

def send_reset_password_email(request, data: str):
    try:
        logger.info(type(data))
        logger.info(data)
        user = user_checker(request, data)
        if user:
            send_user_email.delay(MailTrigger.RESET_PASSWORD.value, user.id)
            messages.success(request, "Письмо для смены пароля отправлено на вашу почту.")
            return HttpResponseRedirect(f"/profile/{user.username}")
        else:
            return HttpResponse("Пользователь с такими данными не найден. Повторите попытку.")
    except Exception as err:
        logger.error(err)
        return HttpResponse("Ошибка при отправке письма")

def user_checker(request, data: str) -> User or None:
    """Функция принимает в себя либо id пользователя, либо электронную почту и возвращает пользователя, если он есть."""
    try:
        if data.isdigit():
            user = User.objects.filter(id=int(data)).first()
            logger.info(f"Поиск пользователя по id {data}")

        elif is_email(data):
            user = User.objects.filter(email=data).first()
            logger.info(f"Поиск пользователя по email: {data}")

        else:
            user = None
            logger.info(f"Неверный формат данных {data}")

        logger.info(f"Найден пользователь {user}")
        return user

    except Exception as err:
        logger.error(err)
        return None

def is_email(value: str) -> bool:
    try:
        validate_email(value)
        return True
    except ValidationError as err:
        logger.error(err)
        return False

def reset_password_with_email(request):
    if request.method == 'POST':
        form = PasswordForgotForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            send_reset_password_email(request, email)
            return HttpResponse("Письмо для смены пароля отправлено на почту.")

    else:
        form = PasswordForgotForm()

    return render(request, 'reset_password_with_email.html', {'form': form})

def reset_password_form_view(request, user_id):
    allowed_user_id = request.session.get('password_reset_user_id')
    if allowed_user_id != user_id:
        return HttpResponseRedirect("/")

    try:
        user = User.objects.get(pk=user_id)

    except User.DoesNotExist:
        return HttpResponse("Пользователь не найден")

    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            return HttpResponse("Пароль успешно изменён. <a href='/login/'>Войти</a>")

    else:
        form = SetNewPasswordForm()
        return render(request, 'password_change_form.html', {'form': form})

def reset_email_form_view(request, user_id):
    allowed_user_id = request.session.get('email_reset_user_id')
    logger.info(f'Полученный request.session {allowed_user_id}')
    if allowed_user_id != user_id:
        return HttpResponseRedirect("/")

    try:
        user = User.objects.get(pk=user_id)

    except User.DoesNotExist:
        return HttpResponse("Пользователь не найден")

    if request.method == 'POST':
        form = SetNewEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user.set_email(email)
            user.save()
            return HttpResponse("Почта успешно изменена. <a href='/login/'>Войти</a>")

    else:
        form = SetNewPasswordForm()
        return render(request, 'password_change_form.html', {'form': form})