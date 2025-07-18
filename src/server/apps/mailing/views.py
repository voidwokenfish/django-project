from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.http import require_POST
from loguru import logger

from .forms import SubscriptionForm
from .helpers import account_activation_token
from .models import Subscription


@require_POST
def subscribe_email(request):
    form = SubscriptionForm(request.POST)
    if form.is_valid():
        form.save()
        send_mail(
            "Спасибо, что подписались на кошачью образовательную рассылку!",
            "Спасибо, что подписались на кошачью образовательную рассылку!",
            settings.EMAIL_HOST_USER, [form.cleaned_data['email']],
            fail_silently=False
        )

    return redirect('index')

def _check_sub(request, email):
    subscription = Subscription.objects.get(email=email)
    if subscription:
        return True
    else:
        return False


User = get_user_model()

def register_confirm(request, uid, token):
    """Функция декодирует данные и завершает регистрацию"""
    uid_decoded = urlsafe_base64_decode(uid).decode()
    user = User.objects.get(pk=uid_decoded) #это я получаю пользователя шоб узнать хто это
    try:
        if user is not None and account_activation_token.check_token(user, token):
            #.check_token сравниваеит данные user и token(там тоже данные user но в токен обернутые)
            user.is_active = True
            user.save()
            return HttpResponseRedirect("/")

        else:
            return HttpResponse("Произошла ошибка.")

    except Exception as err:
        print(err)


def email_confirm(request, uid, token):
    """Функция декодирует данные полученные от """
    try:
        uid_decoded = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid_decoded)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        request.session['email_reset_user_id'] = user.id
        logger.info(f'Передаем request.session {request.session}')
        return HttpResponseRedirect(reverse("reset_email_form_view", args=[user.id]))
    else:
        return HttpResponse("Ссылка недействительна или устарела.")




def reset_password(request, uid, token):
    """Функция декодирует данные и перенаправляет пользователя на страницу смены пароля"""
    try:
        uid_decoded = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid_decoded)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        request.session['password_reset_user_id'] = user.id
        logger.info(f'Передаем request.session {request.session}')
        return HttpResponseRedirect(reverse("reset_password_form_view", args=[user.id]))
    else:
        return HttpResponse("Ссылка недействительна или устарела.")