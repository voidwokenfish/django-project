# Generated by Django 5.1.7 on 2025-03-25 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video_url',
            field=models.URLField(blank=True),
        ),
    ]
