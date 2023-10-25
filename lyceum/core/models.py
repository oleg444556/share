import django.db

__all__ = ["NamePulbishedModel"]


class NamePulbishedModel(django.db.models.Model):
    name = django.db.models.CharField(
        "название",
        help_text="Не более 150 символов",
        max_length=150,
        unique=True,
    )
    is_published = django.db.models.BooleanField(
        "опубликовано",
        help_text="Статус товара",
        default=True,
    )

    class Meta:
        abstract = True
