# Generated by Django 5.1.7 on 2025-04-03 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0004_userquizattempt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizanswer',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='quizquestion',
            name='question',
        ),
        migrations.AddField(
            model_name='quizanswer',
            name='text',
            field=models.CharField(default='Empty Field', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quizquestion',
            name='text',
            field=models.CharField(default='Empty', max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='quiz',
            name='title',
            field=models.CharField(max_length=300),
        ),
    ]
