from django.contrib.auth import get_user_model
from loguru import logger

from server import celery_app
from server.apps.mailing.enums import RecipientType, SendingStatus
from server.apps.mailing.models import EmailLetter, EmailLog, Subscription
from server.apps.news.enums import NotificationStatus
from server.services.mails.enums import MailTrigger
from server.services.mails.utils import MailConstructor, send_mail


@celery_app.app.task()
def send_emails() -> None:
    """Задача рассылки email сообщений"""
    logger.info("Запуск задачи рассылки сообщений")
    mails = EmailLetter.objects.filter(ready_to_send=True, is_processed=False)
    if not mails.exists():
        return logger.info("Завершена задача рассылки. Рассылок нет.")

    count = mails.count()
    for mail in mails:
        news = mail.news if mail.news else None
        attachments = [attachment.file for attachment in mail.attachments.all()]
        if news:
            attachments.extend([attachment.image for attachment in news.images.all()])
        subs = mail.recipient_list.all()
        if not subs:
            match mail.recipient_type:
                case RecipientType.ALL.value:
                    subs = Subscription.objects.filter(is_active=True)
                case RecipientType.REGISTERED.value:
                    subs = Subscription.objects.filter(is_active=True).exclude(user=None)

        for sub in subs:
            try:
                mail_data = MailConstructor(
                    user=None,
                    trigger=MailTrigger.MAIL_LETTER.value,
                    email=sub.email,
                    subject=mail.subject,
                    body=mail.body,
                    attachments=attachments
                ).get_data()
                send_mail(**mail_data, mass_mail=True)

            except Exception as err:
                EmailLog.objects.create(
                    letter=mail, email=sub.email, sending_status=SendingStatus.ERROR, error=err
                    )
                logger.error(f'Ошибка при отправке email сообщения: {err}')

            else:
                EmailLog.objects.create(
                    letter=mail, email=sub.email, sending_status=SendingStatus.SUCCESS
                )

        if news:
            news.notification_status = NotificationStatus.IS_SENT
            news.save(update_fields=['notification_status'])

        mail.is_processed = True
        mail.save(update_fields=['is_processed'])

        logger.info(f"Завершена задача рассылки email сообщений. Обработанно {count} объектов.")

@celery_app.app.task()
def send_user_email(trigger: MailTrigger, user_id: int) -> None:
    """Задача отправки писем пользователям по триггерам:
     RESET_PASSWORD, REGISTER_CONFIRM, MAIL_CONFIRM, GREETING, SUPPORT_RESPONSE"""
    User = get_user_model()
    user = User.objects.get(id=user_id)
    # trigger = MailTrigger(trigger_value)

    logger.info(f'Запуск задачи отправки письма пользователю {user} по триггеру {trigger}')

    try:
        mail_data = MailConstructor(
            user=user,
            trigger=trigger,
            email=user.email,
            subject=None,
            body=None,
            attachments=None
        ).get_data()
        send_mail(**mail_data)

    except Exception as err:
        logger.error(f'Ошибка при отправке email сообщения: {err}')

    else:
        logger.success(f'Успешно отправлено email сообщение для пользователя {user.id} по триггеру {trigger}')
