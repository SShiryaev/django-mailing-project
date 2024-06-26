# Generated by Django 5.0.3 on 2024-04-17 13:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(max_length=500, verbose_name='содержание'),
        ),
        migrations.AlterField(
            model_name='message',
            name='theme',
            field=models.CharField(max_length=100, verbose_name='тема'),
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_at', models.DateTimeField(blank=True, null=True, verbose_name='первая отправка')),
                ('periodicity', models.CharField(choices=[('once_day', 'раз в день'), ('once_week', 'раз в неделю'), ('once_month', 'раз в месяц')], max_length=10, verbose_name='периодичность')),
                ('status', models.CharField(choices=[('created', 'создана'), ('launched', 'запущена'), ('completed', 'завершена')], max_length=9, verbose_name='статус')),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.message', verbose_name='сообщение')),
                ('send_to', models.ManyToManyField(to='mailing.client', verbose_name='получатель')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
            },
        ),
    ]
