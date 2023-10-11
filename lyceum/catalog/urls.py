from django.urls import path, re_path, register_converter

from . import converters, views


register_converter(converters.PositiveNumbersConverter, "pos_int")

urlpatterns = [
    path("", views.item_list),
    path("<int:pk>/", views.item_detail),
    re_path(r"^re/(?P<num>[1-9]\d*)/$", views.catalog_int_pos_num),
    path("converter/<pos_int:num>/", views.catalog_int_pos_num),
]
