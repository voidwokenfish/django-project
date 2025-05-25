from django.db import models
from django.template.context_processors import request

from .enums import RecipientType, SendingStatus
from news.models import News
from django.contrib.auth import get_user_model


User = get_user_model()

class Subscription(models.Model):
    email = models.EmailField(null=False, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='subscription')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Подписка на рассылку"
        verbose_name_plural = "Подписки на рассылку"

class EmailLetter(models.Model):
    subject = models.CharField(max_length=100)
    body = models.TextField()
    recipient_type = models.CharField(choices=RecipientType.choices, default=None, null=True, blank=True)
    ready_to_send = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False) #находится в обработке celery
    created_at = models.DateTimeField(auto_now_add=True)
    recipient_list = models.ManyToManyField(to=Subscription, blank=True)
    news = models.OneToOneField(to=News, null=True, blank=True, on_delete=models.SET_NULL)

class EmailLog(models.Model):
    letter = models.ForeignKey(EmailLetter, on_delete=models.CASCADE, related_name='logs')
    email = models.EmailField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sending_status = models.CharField(choices=SendingStatus.choices, null=True, blank=True)
    error = models.TextField(null=True, blank=True)

class EmailAttachment(models.Model):
    email = models.ForeignKey(EmailLetter, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='email/%Y/%m/%d')