import django.db
from django.http import HttpResponse
import django.shortcuts

import catalog.models
from homepage import forms

__all__ = []


def home(request):
    template = "homepage/home.html"
    items = catalog.models.Item.objects.on_main().order_by("name")
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def coffee_endpoint(request):
    return HttpResponse("Я чайник", status=418)


def echo_submit(request):
    template = "homepage/echo.html"
    form = forms.EchoForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            text = form.cleaned_data.get("text")
            context = {"text": text}
            return django.shortcuts.render(
                request,
                "homepage/echo_submit.html",
                context,
            )

    context = {"form": form}
    return django.shortcuts.render(request, template, context)
