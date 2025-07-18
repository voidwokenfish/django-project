from django.db import models
from solo.models import SingletonModel


class Configuration(SingletonModel):
    """Модель настроек."""

    demo_text = models.TextField(verbose_name="Описание", default="Демонстрационные материалы")
    demo_tg = models.CharField(verbose_name="Telegram-канал", null=True, blank=True, max_length=255)
    demo_youtube = models.URLField(verbose_name="Youtube", null=True, blank=True)
    demo_vk_video = models.URLField(verbose_name="VK Video", null=True, blank=True)

    def __str__(self):
        return 'Настройки'

    class Meta:
        verbose_name = 'Настройки'
