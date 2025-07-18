from django.contrib.auth import get_user_model
from django.test import TestCase
from loguru import logger

from server.apps.periodic_tasks.tasks import send_user_email
from server.services.mails.enums import MailTrigger
from server.services.mails.utils import send_mail

User = get_user_model()

class UserMailTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='voidwokenfish@gmail.com',
            password='Abobus12345'
        )
        self.user.save()

    def test_send_user_email(self):
        send_user_email.delay(MailTrigger.REGISTER_CONFIRM.value, self.user.id)


class SendMailTest(TestCase):

    def test_send_email(self):

        try:
            send_mail(
                subject_template="auth/register_confirm/register_confirm_body.html",
                message_template="auth/register_confirm/register_confirm_sub.txt",
                recipient="voidwokenfish@gmail.com",
                message_context={},
            )
        except Exception as err:
            logger.error(f'Ошибка при отправке email сообщения: {err}')

        else:
            logger.success(f'Успешно отправлено email сообщение')
