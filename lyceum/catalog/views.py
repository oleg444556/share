import django.db
import django.shortcuts

import catalog.models

__all__ = []


def item_list(request):
    template = "catalog/item_list.html"
    items = (
        catalog.models.Item.objects.select_related("category")
        .prefetch_related(
            django.db.models.Prefetch(
                "tags",
                queryset=catalog.models.Tag.objects.filter(
                    is_published=True,
                ).only("name"),
            ),
        )
        .filter(category__is_published=True)
        .filter(is_published=True)
        .only("name", "text", "category__name")
        .order_by("category__name")
    )
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def item_detail(request, pk):
    template = "catalog/item.html"
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects.select_related("category")
        .prefetch_related(
            django.db.models.Prefetch(
                "tags",
                queryset=catalog.models.Tag.objects.filter(
                    is_published=True,
                ).only("name"),
            ),
        )
        .prefetch_related(
            django.db.models.Prefetch(
                "images",
                queryset=catalog.models.ItemImage.objects.only(
                    "item_id",
                    "image",
                ),
            ),
        )
        .select_related("main_image")
        .filter(category__is_published=True)
        .filter(is_published=True)
        .only("name", "text", "category__name", "main_image__image"),
        id=pk,
    )
    context = {"item": item}
    return django.shortcuts.render(request, template, context)
