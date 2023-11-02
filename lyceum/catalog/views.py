import django.shortcuts

__all__ = [
    "item_detail",
    "item_list",
]


def item_list(request):
    template = "catalog/item_list.html"
    return django.shortcuts.render(request, template)


def item_detail(request, pk):
    template = "catalog/item.html"
    return django.shortcuts.render(request, template)
