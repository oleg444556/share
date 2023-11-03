import django.db
from django.http import HttpResponse
import django.shortcuts

import catalog.models

__all__ = []


# Create your views here.
def home(request):
    template = "homepage/home.html"
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
        .filter(is_on_main=True)
        .only("name", "text", "category__name")
        .order_by("name")
    )
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def coffee_endpoint(request):
    return HttpResponse("Я чайник", status=418)
