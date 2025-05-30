from loguru import logger

from coursenator70000 import celery_app
from mailing.models import EmailLetter


@celery_app.app.task()
def send_email() -> None:
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
                case recipient_type.all.value:
                    subs = subscription.objects.filter(is_active=True)
                case 20:
                    print("backflip")



