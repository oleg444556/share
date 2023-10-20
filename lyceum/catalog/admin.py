from django.contrib import admin, messages
import django.core.validators

import catalog.models


@admin.register(catalog.models.Tag)
class TagAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except django.core.exceptions.ValidationError:
            messages.error(request, "Тег с похожим названием уже существует")


@admin.register(catalog.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except django.core.exceptions.ValidationError:
            messages.error(
                request, "Категория с похожим названием уже существует"
            )


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
