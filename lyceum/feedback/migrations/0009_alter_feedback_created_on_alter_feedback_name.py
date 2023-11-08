# Generated by Django 4.2.5 on 2023-11-08 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0008_alter_feedback_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, help_text='Время создания письма', verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='name',
            field=models.CharField(blank=True, help_text='Введите ваше имя (необязательно)', max_length=200, verbose_name='имя отправителя'),
        ),
    ]
