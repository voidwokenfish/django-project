from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponseRedirect

from .forms import RegisterForm, LoginForm, ProfileAvatarForm

from .models import Profile
from courses.models import Course, Enrollment
from django.contrib import auth, messages
from django.urls import reverse

from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            send_mail("Успешная регистрация!", "Вы молодец!", settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
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
