from django.http import HttpResponse


# Create your views here.
def description(request):
    return HttpResponse("<body>О проекте</body>")
