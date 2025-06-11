from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from courses.models import Course, Enrollment

from loguru import logger

from .forms import LoginForm, ProfileAvatarForm, RegisterForm
from .models import Profile

from periodic_tasks.tasks import send_user_email
from services.mails.enums import MailTrigger

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

def send_reset_password_email(request, user_id_or_email: str | int):
    try:
        user = user_checker(request, user_id_or_email)
        if user:
            send_user_email.delay(MailTrigger.RESET_PASSWORD.value, user.id)
            return HttpResponseRedirect(f"/profile/{user.username}")
        else:
            return HttpResponse("Пользователь с такими данными не найден. Повторите попытку.")
    except Exception as err:
        logger.error(err)
        return HttpResponse("Ошибка при отправке письма")

def user_checker(request, data: int | str) -> User or None:
    """Функция принимает в себя либо id пользователя, либо электронную почту и возвращает пользователя, если он есть."""
    try:
        if validate_email(data):
            user = User.objects.filter(email=data).first()

        else:
            user = User.objects.get(username=data)

        return user if user else None

    except ValidationError as err:
        logger.error(err)