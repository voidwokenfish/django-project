# Generated by Django 5.1.7 on 2025-03-12 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, default='defaultpfp.jpg', null=True, upload_to='courses_images/'),
        ),
    ]
