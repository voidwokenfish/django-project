from loguru import logger
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from yookassa.domain.notification import WebhookNotification

import json

from server.apps.courses.models import Course, Enrollment


from server.apps.transactions.models import Transaction
from server.apps.transactions.enums import PaymentStatus

from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class YookassaWebHookView(APIView):
    """Класс-вью обработки вебхука от ЮКасса."""

    def post(self, request, *args, **kwargs):
        """Принимает хук запросы."""
        json_string = request.body.decode('utf-8')
        data = json.loads(json_string)
        logger.info("Запуск вью Юкассы")
        logger.info(data)

        try:
            notification_object = WebhookNotification(data)
            payment = notification_object.object

            if notification_object.event == 'payment.succeeded':
                obj = Transaction.objects.filter(payment_id=payment.id, status=PaymentStatus.NEW.value).first()
                if obj:
                    obj.status = PaymentStatus.SUCCESS
                    obj.error_description = None
                    obj.save(update_fields=['status', 'error_description'])
                    try:
                        user_id = payment.metadata.get('user_id')
                        course_id = payment.metadata.get('course_id')
                        user = get_user_model().objects.get(id=user_id)
                        course = Course.objects.get(id=course_id)
                        Enrollment.objects.create(
                            user=user,
                            course=course,
                            enroll_date=timezone.now().date()
                        )
                        logger.info(f"Создана запись на курс {course.id} для юзера с id {user.id}")
                    except Exception as e:
                        logger.error(f"Ошибка создания Enrollment {e}")

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


