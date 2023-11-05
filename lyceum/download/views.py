import django.conf
import django.http

__all__ = []


def download_image(request, path):
    media_path = django.conf.settings.MEDIA_ROOT / path

    return django.http.FileResponse(open(media_path, "rb"), as_attachment=True)
