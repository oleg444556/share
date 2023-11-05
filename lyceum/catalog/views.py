import datetime
import random

import django.db
import django.shortcuts

import catalog.models

__all__ = []


def item_list(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.published().order_by("category__name")
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def item_detail(request, pk):
    template = "catalog/item.html"
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects.published()
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
        .only("name", "text", "category__name", "main_image__image"),
        id=pk,
    )
    context = {"item": item}
    return django.shortcuts.render(request, template, context)


def new_items(request):
    template = "catalog/cool_item_list.html"
    current_date = datetime.datetime.now()

    one_week_ago = current_date - datetime.timedelta(days=7)

    new_items_ids = list(
        catalog.models.Item.objects.published()
        .filter(
            created_at__range=(one_week_ago, current_date),
        )
        .values_list("id", flat=True),
    )
    try:
        chosen = random.sample(new_items_ids, 5)
    except ValueError:
        chosen = new_items_ids

    items = (
        catalog.models.Item.objects.published()
        .filter(id__in=chosen)
        .order_by(
            "category__name",
        )
    )

    context = {
        "items": items,
        "title": "Новинки",
    }

    return django.shortcuts.render(request, template, context)


def friday_items(request):
    template = "catalog/cool_item_list.html"
    items = (
        catalog.models.Item.objects.published()
        .filter(
            updated_at__week_day=6,
        )
        .order_by("-updated_at")[:5]
    )
    context = {
        "items": items,
        "title": "Пятница",
    }
    return django.shortcuts.render(request, template, context)


def unverified(request):
    template = "catalog/cool_item_list.html"
    items = catalog.models.Item.objects.published().filter(
        updated_at__range=(
            django.db.models.F("created_at") - datetime.timedelta(seconds=1),
            django.db.models.F("created_at") + datetime.timedelta(seconds=1),
        ),
    )
    context = {
        "items": items,
        "title": "Непроверенное",
    }
    return django.shortcuts.render(request, template, context)
