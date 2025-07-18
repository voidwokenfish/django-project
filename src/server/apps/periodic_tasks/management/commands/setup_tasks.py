from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class Command(BaseCommand):
    """Команда для создания переодических задач"""
    help = "Команда для создания переодических задач"

    def handle(self, *args, **options):
        """Консольный вывод команды"""
        self.stdout.write("Начато создание переодических задач: \n")
        start = timezone.now()
        self._setup_tasks()
        self.stdout.write(f"Переодические задачи созданы. Время: {(timezone.now() - start).seconds / 60:.2f} мин.")

    def _setup_tasks(self):
        """Переодические задачи"""
        every_one_hour_cron, _ = CrontabSchedule.objects.get_or_create(
            minute="*/60", timezone=settings.TIME_ZONE
        ) # get_or_create возвращает объект и True or False - данные идут в every_one_hour_cron, а true/false в _
        _ = PeriodicTask.objects.update_or_create(
            name="Отправка email писем готовых к отправке",
            defaults={
                "crontab": every_one_hour_cron,
                "task": "src.periodic_tasks.tasks.send_emails",
            }
        )

        every_three_min_cron, _ = CrontabSchedule.objects.get_or_create(
            minute="*/3", timezone=settings.TIME_ZONE
        )
        _ = PeriodicTask.objects.update_or_create(
            name="Отправка писем пользователям по триггерам: RESET_PASSWORD, REGISTER_CONFIRM, MAIL_CONFIRM, GREETING, SUPPORT_RESPONSE",
            defaults={
                "crontab": every_three_min_cron,
                "task": "src.periodic_tasks.tasks.send_user_email",
            }
        )
