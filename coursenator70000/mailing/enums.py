from django.db import models

class SendingStatus(models.TextChoices):
    SUCCESS = 'success', 'Отправлено успешно'
    ERROR = 'error', 'Ошибка при отправке'

class RecipientType(models.TextChoices):
    REGISTERED = 'registered', 'Зарегистрированным'
    ALL = 'all', 'Всем'

