from django.http import HttpResponse


# Create your views here.
def item_list(request):
    return HttpResponse("<body>Список элементов</body>")


def item_detail(request, pk):
    return HttpResponse("<body>Подробно элемент</body>")


def catalog_int_pos_num(request, num):
    return HttpResponse(f"<body>{num}</body>")


def catalog_converter_int_pos(request, num):
    return HttpResponse(f"<body>{num}</body>")
