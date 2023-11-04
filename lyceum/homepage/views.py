import django.db
from django.http import HttpResponse
import django.shortcuts

import catalog.models

__all__ = []


# Create your views here.
def home(request):
    template = "homepage/home.html"
    items = catalog.models.Item.objects.on_main().order_by("name")
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def coffee_endpoint(request):
    return HttpResponse("Я чайник", status=418)
