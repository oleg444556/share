import django.db
from django.http import HttpResponse
import django.shortcuts
from django.views.decorators.http import require_POST, require_GET

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


@require_GET
def echo(request):
    template = "homepage/echo.html"
    form = forms.EchoForm()
    context = {"form": form}

    return django.shortcuts.render(request, template, context)


@require_POST
def echo_submit(request):
    template = "homepage/echo_submit.html"
    form = forms.EchoForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            text = form.cleaned_data.get("text")
            context = {"text": text}

    return django.shortcuts.render(request, template, context)
