import django.shortcuts

__all__ = []


def description(request):
    template = "about/about.html"
    context = {}
    return django.shortcuts.render(request, template, context)
