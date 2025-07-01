from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from loguru import logger

from server.apps.mailing.helpers import account_activation_token

from .enums import MailTrigger

User = get_user_model()


class MailConstructor:
    """Письма дкелаентб"""
    def __init__(
            self,
            user: User | None,
            trigger: MailTrigger,
            email: str | None=None,
            subject: str | None=None,
            body: str | None=None,
            attachments: list | None=None,
    ):
        self.user = user
        self.trigger = trigger
        self.email = email
        self.subject = subject
        self.body = body
        self.attachments = attachments
        self._data = {}

    def get_data(self) -> dict:
        trigger_map = {
            MailTrigger.GREETING.value: self._greeting_data,
            MailTrigger.SUPPORT_RESPONSE.value: self._support_response_data,
            MailTrigger.REGISTER_CONFIRM.value: self._register_confirm_data,
            MailTrigger.RESET_PASSWORD.value: self._reset_password_data,
            MailTrigger.MAIL_CONFIRM.value: self._mail_confirm_data,
            MailTrigger.MAIL_LETTER.value: self._mail_letter_data,
        }

        self._add_common()

        trigger_map[self.trigger]()

        return self._data

    def _add_common(self):
        """Метод формирования общего контекста"""
        self._data.update(
            {
                "message_context": {"SITE_URL": settings.SITE_URL, },
                "recipient": self.user.email if self.user else self.email
            })

    def _greeting_data(self):
        """Метод формирования данных для триггера 'GREETENG'"""
        template_path = 'auth/greeting'
        self._data.update({
            "subject_template": f"{template_path}/greeting_sub.txt",
            "message_template": f"{template_path}/greeting_body.html",
        })

    def _mail_letter_data(self):
        """Метод формирования данных для триггера 'MAIL_LETTER'"""
        self._data.update({
            "subject_template": self.subject,
            "message_template": self.body,
            "attachments": self.attachments,
        })

    def _support_response_data(self):
        """Метод формирования данных для триггера 'SUPPORT_RESPONSE'"""
        self._data.update({
            "subject_template": self.subject,
            "message_template": self.body,
        })

    def _register_confirm_data(self):
        """Метод формирования данных для триггера 'REGISTER_CONFIRM'"""
        template_path = 'auth/register_confirm'
        self._data.update({
            "subject_template": f"{template_path}/register_confirm_sub.txt",
            "message_template": f"{template_path}/register_confirm_body.html",
        })
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)
        endpoint = f"{settings.SITE_URL.rstrip('/')}{reverse('mailing:register_confirm', kwargs={'uid': uid, 'token': token})}"
        logger.info(f"SITE_URL: '{settings.SITE_URL}'")
        logger.info(f"Endpoint: '{endpoint}'")
        self._data["message_context"].update({
            "uid": uid,
            "token": token,
            "endpoint": endpoint,
        })

    def _reset_password_data(self):
        """Метод формирования данных для триггера 'RESET_PASSWORD'"""
        template_path = 'auth/reset_password'
        self._data.update({
            "subject_template": f"{template_path}/reset_password_sub.txt",
            "message_template": f"{template_path}/reset_password_body.html",
        })
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)
        endpoint = f"{settings.SITE_URL.rstrip('/')}{reverse('mailing:reset_password', kwargs={'uid': uid, 'token': token})}"
        self._data["message_context"].update({
            "uid": uid,
            "token": token,
            "endpoint": endpoint,
        })

    def _mail_confirm_data(self):
        """Метод формирования данных для триггера 'MAIL_CONFIRM'"""
        template_path = 'auth/mail_confirm'
        self._data.update({
            "subject_template": f"{template_path}/mail_confirm_sub.txt",
            "message_template": f"{template_path}/mail_confirm_body.html",
        })

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)
        endpoint = f"{settings.SITE_URL.rstrip('/')}{reverse('mailing:email_confirm', kwargs={'uid':uid, 'token':token})}"
        self._data["message_context"].update({
            "uid": uid,
            "token": token,
            "endpoint": endpoint,
        })


def send_mail(
    subject_template: str,
    message_template: str,
    recipient: str,
    message_context: dict,
    mass_mail: bool = False,
    attachments: list | None = None,
):
    if mass_mail:
        subject = subject_template
        body = message_template

    else:
        subject = render_to_string(subject_template)
        subject = "".join(subject.splitlines())
        body = render_to_string(message_template, message_context)

    mail = EmailMessage(
        subject=subject,
        body=body,
        to=[recipient],
    )

    if attachments:
        for attachment in attachments:
            mail.attach_file(attachment.path)

    mail.content_subtype = 'html'
    mail.send()