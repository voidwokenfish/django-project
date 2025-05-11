from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from .forms import SubscriptionForm
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