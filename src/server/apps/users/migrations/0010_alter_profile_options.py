# Generated by Django 5.1.7 on 2025-04-26 00:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Профиль', 'verbose_name_plural': 'Профили'},
        ),
    ]
