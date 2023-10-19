# Generated by Django 4.2.5 on 2023-10-19 14:02

import catalog.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "catalog",
            "0001_squashed_0005_alter_category_options_alter_item_options_and_more_squashed_0006_alter_tag_options_alter_category_is_published_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="text",
            field=models.TextField(
                help_text="Описание товара, обязательно должно входить одно из слов:превосходно, роскошно",
                validators=[
                    catalog.models.ValidateMustContain("превосходно", "роскошно")
                ],
                verbose_name="текст",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="text",
            field=models.TextField(
                help_text="Описание товара, обязательно должно входить одно из слов:превосходно, роскошно",
                validators=[
                    catalog.models.ValidateMustContain(
                        "превосходно", "роскошно", "унинянимонини"
                    )
                ],
                verbose_name="текст",
            ),
        ),
    ]
