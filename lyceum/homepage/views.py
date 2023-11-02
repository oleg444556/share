from django.http import HttpResponse
import django.shortcuts

__all__ = []


# Create your views here.
def home(request):
    template = "homepage/home.html"
    context = {}
    return django.shortcuts.render(request, template, context)


def coffee_endpoint(request):
    return HttpResponse("Я чайник", status=418)
