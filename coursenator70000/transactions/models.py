from django.db import models

from courses.models import Course
from transactions.enums import PaymentStatus
from users.models import User


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255, null=True)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=100, null=True, choices=PaymentStatus.choices, default=PaymentStatus.NEW)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    idempotence_key = models.CharField(max_length=255, null=True)
    error_description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
