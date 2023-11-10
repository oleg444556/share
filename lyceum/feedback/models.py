from django.conf import settings
import django.db
import django.utils.timezone

__all__ = ["Feedback", "StatusLog"]


class Feedback(django.db.models.Model):
    STATUS_CHOICES = [
        ("GOT", "получено"),
        ("IN", "в обработке"),
        ("OK", "ответ дан"),
    ]
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
    )

    class Meta:
        verbose_name = "фидбек"
        verbose_name_plural = "фидбек"

    def __str__(self):
        return self.display_name()

    def display_name(self):
        return self.personal.name if self.personal.name else "Без имени"

    def display_mail(self):
        return self.personal.mail if self.personal.mail else "Без mail"

    display_name.short_description = "имя отправителя"
    display_name.allow_tags = True

    display_mail.short_description = "почта отправителя"
    display_mail.allow_tags = True


class StatusLog(django.db.models.Model):
    user = django.db.models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=django.db.models.SET_NULL,
        verbose_name="пользователь",
        null=True,
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


class FeedbackPersonal(django.db.models.Model):
    text_feedback = django.db.models.OneToOneField(
        "Feedback",
        on_delete=django.db.models.CASCADE,
        null=True,
        verbose_name="пероснальные данные",
        related_name="personal",
    )
    mail = django.db.models.EmailField(
        "почта",
        help_text="Введите вашу почту",
    )
    name = django.db.models.CharField(
        "имя отправителя",
        help_text="Введите ваше имя (необязательно)",
        max_length=200,
        blank=True,
    )

    class Meta:
        verbose_name = "персональные данные"
        verbose_name_plural = "персональные данные"

    def __str__(self):
        return self.mail


class FeedbackFiles(django.db.models.Model):
    def get_upload_path(self, filename):
        return f"uploads/{self.main_feedback_id}/{filename}"

    main_feedback = django.db.models.ForeignKey(
        "Feedback",
        on_delete=django.db.models.CASCADE,
        verbose_name="файл",
        related_query_name="files",
    )
    file = django.db.models.FileField(
        "файл",
        upload_to=get_upload_path,
        null=True,
    )
