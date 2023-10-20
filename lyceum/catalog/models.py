import django.core.validators
import django.db

import catalog.utils
import catalog.validators
import core.models


class Item(core.models.NamePulbishedModel):
    text = django.db.models.TextField(
        "текст",
        help_text="Описание товара, обязательно должно входить одно из слов:"
        "превосходно, роскошно",
        validators=[
            catalog.validators.ValidateMustContain(
                "превосходно", "роскошно", "унинянимонини"
            ),
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
    normalized_name = django.db.models.SlugField(
        "нормализованное имя",
        help_text="Нормализованное имя необходимое для "
        "исключения похожих названий",
        unique=True,
        editable=False,
    )
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

    def full_clean(self, *args, **kwargs):
        try:
            self.normalized_name = catalog.utils.name_slugify(self.name)
            super().full_clean(*args, **kwargs)
        except django.db.IntegrityError:
            raise django.core.exceptions.ValidationError(
                "Тег с похожим именем уже существует"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Category(core.models.NamePulbishedModel):
    normalized_name = django.db.models.SlugField(
        "нормализованное имя",
        help_text="Нормализованное имя необходимое для "
        "исключения похожих названий",
        unique=True,
        editable=False,
    )
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

    def full_clean(self, *args, **kwargs):
        try:
            self.normalized_name = catalog.utils.name_slugify(self.name)
            super().full_clean(*args, **kwargs)
        except django.db.IntegrityError:
            raise django.core.exceptions.ValidationError(
                "Категория с похожим именем уже существует"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
