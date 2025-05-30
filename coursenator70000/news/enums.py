from django.db import models


class NotificationStatus(models.TextChoices):
    NOT_SEND = 'not_send', 'Не уведомлять'
    TO_SEND = 'to_send', 'Уведомить'
    IS_SENT = 'is_sent', 'Уведомление отправлено'


"""
from django.db import models

class SendingStatus(models.TextChoices):
    SUCCESS = 'success', 'Отправлено успешно'
    ERROR = 'error', 'Ошибка при отправке'

class RecipientType(models.TextChoices):
    REGISTERED = 'registered', 'Зарегистрированным'
    ALL = 'all', 'Всем'
    
В енамку mailing
"""