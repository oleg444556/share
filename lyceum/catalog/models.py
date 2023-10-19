import re

import django.core.exceptions
import django.core.validators
import django.db

import core.models


def validate_must_contain(value):
    pattern = r"\b(превосходно|роскошно)\b"
    if not re.search(pattern, value.lower()):
        raise django.core.exceptions.ValidationError(
            "В тексте должно быть слово 'превосходно' или 'роскошно'"
        )


class Item(core.models.NamePulbishedModel):
    text = django.db.models.TextField(
        "текст",
        help_text="Описание товара, обязательно должно входить одно из слов:"
        "превосходно, роскошное",
        validators=[
            validate_must_contain,
        ],
    )
    tags = django.db.models.ManyToManyField("tag", verbose_name="тэги")
    category = django.db.models.ForeignKey(
        "category",
        on_delete=django.db.models.CASCADE,
        verbose_name="категория",
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name


class Tag(core.models.NamePulbishedModel):
    slug = django.db.models.SlugField(
        "слаг",
        help_text="Максимальная длина - 200 символов, уникальное значение "
        "в рамках таблицы, только цифры, буквы латиницы и символы - и _",
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name


class Category(core.models.NamePulbishedModel):
    slug = django.db.models.SlugField(
        "слаг",
        help_text="Максимальная длина 200 символов, уникальное значение"
        "рамках таблицы, только цифры буквы латиницы и символы - и _",
        max_length=200,
        unique=True,
    )
    weight = django.db.models.SmallIntegerField(
        "вес",
        help_text="От 1 до 32767, значение по-умолчанию 100, целое число",
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
        default=100,
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name
