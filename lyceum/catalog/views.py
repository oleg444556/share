from django.http import HttpResponse
import django.shortcuts

__all__ = [
    "catalog_converter_int_pos",
    "catalog_int_pos_num",
    "item_detail",
    "item_list",
]


def item_list(request):
    template = "catalog/item_list.html"
    context = {}
    return django.shortcuts.render(request, template, context)


def item_detail(request, pk):
    template = "catalog/item.html"
    context = {}
    return django.shortcuts.render(request, template, context)


def catalog_int_pos_num(request, num):
    return HttpResponse(f"<body>{num}</body>")


def catalog_converter_int_pos(request, num):
    return HttpResponse(f"<body>{num}</body>")
