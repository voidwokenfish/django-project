import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.server.settings')

app = Celery('server')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'UTC'