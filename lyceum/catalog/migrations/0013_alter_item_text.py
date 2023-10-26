# Generated by Django 4.2.5 on 2023-10-26 14:23

import catalog.validators
import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0012_alter_mainimage_options_alter_itemimage_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="text",
            field=ckeditor.fields.RichTextField(
                help_text="Описание товара, обязательно должно входить одно из слов:превосходно, роскошно",
                validators=[
                    catalog.validators.ValidateMustContain(
                        "превосходно", "роскошно", "унинянимонини"
                    )
                ],
                verbose_name="текст",
            ),
        ),
    ]
