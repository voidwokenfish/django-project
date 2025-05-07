from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .forms import SubscriptionForm

@require_POST
def subscribe_email(request):
    form = SubscriptionForm(request.POST)
    if form.is_valid():
        form.save()

    return redirect('index')