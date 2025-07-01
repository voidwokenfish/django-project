from django.db import models

class PaymentStatus(models.TextChoices):
    """Статус платежа"""
    NEW = "NEW", "Новый"
    SUCCESS = "SUCCESS", "Успешно"
    ERROR = "ERROR", "Ошибка"