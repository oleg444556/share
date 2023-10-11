from django.http import HttpResponse


# Create your views here.
def home(request):
    return HttpResponse("<body>Главная</body>")


def coffee_endpoint(request):
    return HttpResponse("Я чайник", status=418)
