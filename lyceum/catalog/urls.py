from django.urls import path, register_converter

from catalog import converters, views


register_converter(converters.PositiveNumbersConverter, "pos_int")

app_name = "catalog"

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("<int:pk>/", views.item_detail, name="item_detail"),
    path("new/", views.new_items, name="new"),
    path("friday/", views.friday_items, name="friday"),
    path("unverified/", views.unverified, name="unverified"),
]
