import ckeditor.fields
import django.core.validators
import django.db
import django.utils.safestring
import sorl.thumbnail

import catalog.utils
import catalog.validators
import core.models

__all__ = ["Category", "Item", "ItemImage", "Tag"]


class ItemManager(django.db.models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .select_related("category")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=Tag.objects.filter(
                        is_published=True,
                    ).only("name"),
                ),
            )
            .filter(category__is_published=True)
            .filter(is_published=True)
            .only(
                "name",
                "text",
                "category__name",
            )
        )

    def on_main(self):
        return (
            self.get_queryset()
            .select_related("category")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=Tag.objects.filter(
                        is_published=True,
                    ).only("name"),
                ),
            )
            .filter(category__is_published=True)
            .filter(is_published=True)
            .filter(is_on_main=True)
            .only(
                "name",
                "text",
                "category__name",
            )
        )


class Item(core.models.NamePulbishedModel):
    objects = ItemManager()

    is_on_main = django.db.models.BooleanField(
        "отображается на главной",
        help_text="Статус товара на главной странице",
        default=False,
    )
    text = ckeditor.fields.RichTextField(
        "текст",
        help_text="Описание товара, обязательно должно входить одно из слов:"
        "превосходно, роскошно",
        validators=[
            catalog.validators.ValidateMustContain(
                "превосходно",
                "роскошно",
                "унинянимонини",
            ),
        ],
    )
    tags = django.db.models.ManyToManyField(
        "tag",
        verbose_name="тэги",
        related_query_name="items",
    )
    category = django.db.models.ForeignKey(
        "category",
        on_delete=django.db.models.CASCADE,
        verbose_name="категория",
        related_query_name="items",
    )
    created_at = django.db.models.DateTimeField(
        "время создания",
        help_text="Время создания товара",
        auto_now_add=True,
    )
    updated_at = django.db.models.DateTimeField(
        "время последнего обновления",
        help_text="Время последнего обновления товара",
        auto_now=True,
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name

    def image_tmb(self):
        if self.main_image.image:
            return django.utils.safestring.mark_safe(
                "<img src="
                f"'{self.main_image.get_image_50x50.url}'"
                "width='50'>",
            )
        return "Нет изображения"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True


class MainImage(django.db.models.Model):
    main_item = django.db.models.OneToOneField(
        "Item",
        on_delete=django.db.models.CASCADE,
        null=True,
        verbose_name="главное изображение",
        related_name="main_image",
    )
    image = django.db.models.ImageField(
        "главное изображение",
        upload_to="catalog/",
        null=True,
        blank=True,
        help_text="Загрузите главное изображение товара",
    )

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"

    @property
    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            quality=51,
        )

    @property
    def get_image_50x50(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "50x50",
            quality=51,
        )


class ItemImage(django.db.models.Model):
    item = django.db.models.ForeignKey(
        "item",
        on_delete=django.db.models.CASCADE,
        verbose_name="изображения к товару",
        related_name="images",
    )
    image = django.db.models.ImageField(
        "изображение к товару",
        help_text="Загрузите изображения в галлерею товара",
        upload_to="catalog/",
        null=True,
    )

    class Meta:
        verbose_name = "изображение к товару"
        verbose_name_plural = "изображения к товару"

    @property
    def get_image_50x50(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "50x50",
            quality=51,
        )

    @property
    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            quality=51,
        )


class Tag(core.models.NamePulbishedModel):
    normalized_name = django.db.models.SlugField(
        "нормализованное имя",
        help_text="Нормализованное имя необходимое для "
        "исключения похожих названий",
        unique=True,
        editable=False,
        null=True,
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

    def save(self, *args, **kwargs):
        self.normalized_name = catalog.utils.name_slugify(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        self.normalized_name = catalog.utils.name_slugify(self.name)
        if (
            type(self)
            .objects.filter(normalized_name=self.normalized_name)
            .exclude(id=self.id)
            .count()
            > 0
        ):
            raise django.core.exceptions.ValidationError(
                "Тег с похожим именем уже существует",
            )
        super().clean()


class Category(core.models.NamePulbishedModel):
    normalized_name = django.db.models.SlugField(
        "нормализованное имя",
        help_text="Нормализованное имя необходимое для "
        "исключения похожих названий",
        unique=True,
        editable=False,
        null=True,
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

    def save(self, *args, **kwargs):
        self.normalized_name = catalog.utils.name_slugify(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        self.normalized_name = catalog.utils.name_slugify(self.name)
        if (
            type(self)
            .objects.filter(normalized_name=self.normalized_name)
            .exclude(id=self.id)
            .count()
            > 0
        ):
            raise django.core.exceptions.ValidationError(
                "Категория с похожим именем уже существует",
            )
        super().clean()
