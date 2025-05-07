from django.contrib import admin
from .models import Subscription

@admin.register
class SubscriptionAdmin(Subscription):
    pass
