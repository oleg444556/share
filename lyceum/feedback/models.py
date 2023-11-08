import django.contrib.auth
import django.db
import django.utils.timezone

__all__ = ["Feedback", "StatusLog"]


class Feedback(django.db.models.Model):
    STATUS_CHOICES = {
        ("GOT", "получено"),
        ("IN", "в обработке"),
        ("OK", "ответ дан"),
    }
    status = django.db.models.CharField(
        "статус обращения",
        help_text="Текущий статус полученного письма",
        max_length=4,
        choices=STATUS_CHOICES,
        default="GOT",
    )
    text = django.db.models.TextField(
        "текст письма",
        help_text="Введите текст письма",
    )
    created_on = django.db.models.DateTimeField(
        "время создания",
        help_text="Время создания письма",
        auto_now_add=True,
        null=True,
    )
    mail = django.db.models.EmailField(
        "почта",
        help_text="Введите вашу почту",
    )
    name = django.db.models.CharField(
        "имя отправителя",
        help_text="Введите ваше имя",
        max_length=200,
    )

    class Meta:
        verbose_name = "фидбек"
        verbose_name_plural = "фидбек"

    def __str__(self):
        return self.mail

    def save(self, *args, **kwargs):
        if self.pk and self.user:
            old_feed = Feedback.objects.get(id=self.pk)
            if self.status != old_feed.status:
                StatusLog.objects.create(
                    user=self.user,
                    feedback=self,
                    from_status=old_feed.get_status_display(),
                    to=self.get_status_display(),
                )
        super().save(*args, **kwargs)


class StatusLog(django.db.models.Model):
    user = django.db.models.ForeignKey(
        django.contrib.auth.get_user_model(),
        on_delete=django.db.models.CASCADE,
        verbose_name="пользователь",
    )
    timestamp = django.db.models.DateTimeField(
        "время изменения",
        default=django.utils.timezone.now,
        editable=False,
    )
    feedback = django.db.models.ForeignKey(
        "feedback",
        on_delete=django.db.models.CASCADE,
        verbose_name="фидбек",
        null=True,
    )
    from_status = django.db.models.CharField(
        "изначальный статус",
        help_text="Изначальный статус",
        max_length=12,
        db_column="from",
        null=True,
    )
    to = django.db.models.CharField(
        "текущий статус",
        help_text="Текущий статус",
        max_length=12,
        null=True,
    )

    class Meta:
        verbose_name = "лог статуса"
        verbose_name_plural = "логи статуса"
