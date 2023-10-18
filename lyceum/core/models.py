import django.db


class NamePulbishedModel(django.db.models.Model):
    name = django.db.models.CharField(
        "Название", help_text="Не более 150 символов", max_length=150
    )
    is_published = django.db.models.BooleanField(
        "Опубликовано",
        help_text="Статус товара",
        default=True,
    )

    class Meta:
        abstract = True
