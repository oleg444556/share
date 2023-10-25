from django.contrib import admin

import catalog.models

__all__ = ["CategoryAdmin", "ItemAdmin", "ItemInline", "TagAdmin"]


class ItemInline(admin.TabularInline):
    fk_name = "item"
    model = catalog.models.ItemImage
    extra = 1


@admin.register(catalog.models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(catalog.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
    ]
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        "image_tmb",
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
