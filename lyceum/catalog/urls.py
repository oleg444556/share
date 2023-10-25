from django.urls import path, re_path, register_converter

from catalog import converters, views


register_converter(converters.PositiveNumbersConverter, "pos_int")

app_name = "catalog"

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("<int:pk>/", views.item_detail, name="item_detail"),
    re_path(
        r"^re/(?P<num>[1-9]\d*)/$",
        views.catalog_int_pos_num,
        name="catalog_re",
    ),
    path(
        "converter/<pos_int:num>/",
        views.catalog_converter_int_pos,
        name="catalog_converter",
    ),
]
