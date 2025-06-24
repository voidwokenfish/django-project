from django.shortcuts import render
from loguru import logger
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from yookassa.domain.notification import WebhookNotification

import json

from transactions.models import Transaction
from transactions.enums import PaymentStatus


class YookassaWebHookView(APIView):
    """Класс-вью обработки вебхука от ЮКасса."""

    def post(self, request, *args, **kwargs):
        """Принимает хук запросы."""
        json_string = request.body.decode('utf-8')
        data = json.loads(json_string)

        try:
            notification_object = WebhookNotification(data)
            payment = notification_object.object

            if notification_object.event == 'payment.succeeded':
                obj = Transaction.objects.filter(payment_id=payment.id, status=PaymentStatus.NEW.value).first()
                if obj:
                    obj.status = PaymentStatus.SUCCESS
                    obj.error_description = None
                    obj.save(update_fields=['status', 'error_description'])
                    #todo Сделать зачисление на курс студента.

                    logger.info(f'Осуществлен платеж ID {obj.id} по транзакции {obj.payment_id}')

            if notification_object.event == 'payment.canceled':
                obj = Transaction.objects.filter(payment_id=payment.id).exclude(status=PaymentStatus.SUCCESS).first()
                if obj:
                    obj.status = PaymentStatus.ERROR
                    obj.idempotence_key = None
                    obj.error = payment.cancellation_details.reason
                    obj.save(update_fields=['status', 'error', 'idempotence_key'])

                    logger.info(f'Отменен платеж ID {obj.id} по транзакции {obj.payment_id}')

        except Exception as exc:
            logger.error('Ошибка обработки вебхука: {exc}\ndata\n{data}'.format(exc=exc, data=data))

        return Response(status=status.HTTP_200_OK)


