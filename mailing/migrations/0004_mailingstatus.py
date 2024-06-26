# Generated by Django 5.0.3 on 2024-04-17 14:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0003_alter_message_body_alter_message_theme_mailing'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_try', models.DateTimeField(blank=True, null=True, verbose_name='последняя попытка')),
                ('mailing_status', models.BooleanField(default=False, verbose_name='успешно')),
                ('post_log', models.CharField(blank=True, max_length=200, null=True, verbose_name='ответ почтового сервиса')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'статус рассылки',
                'verbose_name_plural': 'статусы рассылок',
            },
        ),
    ]
