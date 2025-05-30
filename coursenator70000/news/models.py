from django.db import models
from django.utils import timezone

from .enums import NotificationStatus


class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    preview = models.ImageField(upload_to='news/previews/%d/%m/%Y', null=True, blank=True)
    notification_status = models.CharField(choices=NotificationStatus.choices, default=NotificationStatus.NOT_SEND, max_length=100)
    pub_date = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_published:
            self.pub_date = timezone.now()
        else:
            self.pub_date = None

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='news/images/%d/%m/%Y', null=True, blank=True)

    def __str__(self):
        return self.news.title

    class Meta:
        verbose_name = "Изображение для новости"
        verbose_name_plural = "Изображения для новости"
