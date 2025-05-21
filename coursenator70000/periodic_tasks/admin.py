from django.contrib import admin
from django_celery_beat.models import ClockedSchedule, IntervalSchedule, SolarSchedule


admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(IntervalSchedule)