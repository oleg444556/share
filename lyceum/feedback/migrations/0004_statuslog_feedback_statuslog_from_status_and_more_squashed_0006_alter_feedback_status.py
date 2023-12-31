# Generated by Django 4.2.5 on 2023-11-08 16:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_feedback_status_alter_feedback_name_statuslog'),
    ]

    operations = [
        migrations.AddField(
            model_name='statuslog',
            name='feedback',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='feedback.feedback', verbose_name='фидбек'),
        ),
        migrations.AddField(
            model_name='statuslog',
            name='from_status',
            field=models.CharField(db_column='from', help_text='Изначальный статус', max_length=12, null=True, verbose_name='изначальный статус'),
        ),
        migrations.AddField(
            model_name='statuslog',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='время изменения'),
        ),
        migrations.AddField(
            model_name='statuslog',
            name='to_status',
            field=models.CharField(db_column='to', help_text='Текущий статус', max_length=12, null=True, verbose_name='текущий статус'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='status',
            field=models.CharField(choices=[('GOT', 'получено'), ('OK', 'ответ дан'), ('IN', 'в обработке')], default='GOT', help_text='Текущий статус полученного письма', max_length=4, verbose_name='статус обращения'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='status',
            field=models.CharField(choices=[('OK', 'ответ дан'), ('GOT', 'получено'), ('IN', 'в обработке')], default='GOT', help_text='Текущий статус полученного письма', max_length=4, verbose_name='статус обращения'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='status',
            field=models.CharField(choices=[('IN', 'в обработке'), ('OK', 'ответ дан'), ('GOT', 'получено')], default='GOT', help_text='Текущий статус полученного письма', max_length=4, verbose_name='статус обращения'),
        ),
    ]
