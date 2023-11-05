from django.urls import path

from download.views import download_image


app_name = "download"

urlpatterns = [
    path("<path:path>", download_image, name="download"),
]
