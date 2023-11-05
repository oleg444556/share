from django.contrib import admin

import catalog.models

__all__ = []


class ItemInline(admin.TabularInline):
    fk_name = "item"
    model = catalog.models.ItemImage
    extra = 1


class MainImageInline(admin.TabularInline):
    model = catalog.models.MainImage
    extra = 1


@admin.register(catalog.models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Tag.name.field.name,
        catalog.models.Tag.is_published.field.name,
    )
    list_editable = (catalog.models.Tag.is_published.field.name,)
    list_display_links = (catalog.models.Tag.name.field.name,)


@admin.register(catalog.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Category.name.field.name,
        catalog.models.Category.is_published.field.name,
    )
    list_editable = (catalog.models.Category.is_published.field.name,)
    list_display_links = (catalog.models.Category.name.field.name,)


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [
        MainImageInline,
        ItemInline,
    ]
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.is_on_main.field.name,
        catalog.models.Item.image_tmb,
    )
    list_editable = (
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.is_on_main.field.name,
    )
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
    readonly_fields = (
        catalog.models.Item.created_at.field.name,
        catalog.models.Item.updated_at.field.name,
    )
