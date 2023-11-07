import django.db

__all__ = ["Feedback"]


class Feedback(django.db.models.Model):
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

    class Meta:
        verbose_name = "фидбек"
        verbose_name_plural = "фидбек"
