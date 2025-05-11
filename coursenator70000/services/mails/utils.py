from django.contrib.auth import get_user_model
from django.conf import settings
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
            MailTrigger.GREETING.value: self._greeting_data
        }

        self._data.update(
            {
                "message_context":{"SITE_URL": settings.SITE_URL,},
                "recipient": self.user.email if self.user else self.email
            })

        trigger_map[self.trigger]()

    def _greeting_data(self):
        template_path = 'auth/greeting'
        self._data.update({
            "subject_template": f"{template_path}/greeting_sub.txt",
            "message_template": f"{template_path}/greeting_body.html",
        })