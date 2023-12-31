# Generated by Django 4.2.5 on 2023-10-19 12:40

import catalog.models
import catalog.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion

__all__ = ["Migration"]


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Не более 150 символов",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Статус товара",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Максимальная длина 200 символов, уникальное значениерамках таблицы, только цифры буквы латиницы и символы - и _",
                        max_length=200,
                        unique=True,
                        verbose_name="слаг",
                    ),
                ),
                (
                    "weight",
                    models.SmallIntegerField(
                        default=100,
                        help_text="От 1 до 32767, значение по-умолчанию 100, целое число",
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(32767),
                        ],
                        verbose_name="вес",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "verbose_name": "категория",
                "verbose_name_plural": "категории",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Не более 150 символов",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Статус товара",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Максимальная длина - 200 символов, уникальное значение в рамках таблицы, только цифры, буквы латиницы и символы - и _",
                        max_length=200,
                        unique=True,
                        verbose_name="слаг",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "verbose_name": "тег",
                "verbose_name_plural": "теги",
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Не более 150 символов",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Статус товара",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="Описание товара, обязательно должно входить одно из слов:превосходно, роскошное",
                        validators=[catalog.validators.ValidateMustContain],
                        verbose_name="текст",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.category",
                        verbose_name="категория",
                    ),
                ),
                ("tags", models.ManyToManyField(to="catalog.tag", verbose_name="тэги")),
            ],
            options={
                "verbose_name": "товар",
                "verbose_name_plural": "товары",
            },
        ),
    ]
