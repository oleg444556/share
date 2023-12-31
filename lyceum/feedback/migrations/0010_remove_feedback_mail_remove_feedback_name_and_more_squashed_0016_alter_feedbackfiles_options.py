# Generated by Django 4.2.5 on 2023-11-14 21:27

from django.db import migrations, models
import django.db.models.deletion
import feedback.models


class Migration(migrations.Migration):
    dependencies = [
        ('feedback', '0009_alter_feedback_created_on_alter_feedback_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='mail',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='name',
        ),
        migrations.CreateModel(
            name='FeedbackPersonal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.EmailField(help_text='Введите вашу почту', max_length=254, verbose_name='почта')),
                ('name', models.CharField(blank=True, help_text='Введите ваше имя (необязательно)', max_length=200, verbose_name='имя отправителя')),
                ('text_feedback', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personal', to='feedback.feedback', verbose_name='пероснальные данные')),
            ],
            options={
                'verbose_name': 'персональные данные',
                'verbose_name_plural': 'персональные данные',
            },
        ),
        migrations.CreateModel(
            name='FeedbackFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to=feedback.models.FeedbackFiles.get_upload_path, verbose_name='файл')),
                ('feedback', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='file', related_query_name='files', to='feedback.feedback', verbose_name='файл')),
            ],
            options={
                'verbose_name': 'файл фидбека',
                'verbose_name_plural': 'файлы фидбека',
            },
        ),
    ]
