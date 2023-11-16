from django.contrib.auth.middleware import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser

import users.models

__all__ = ["CustomUserMiddleware"]


class CustomUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            request.user = users.models.User.objects.get(id=request.user.id)
        else:
            request.user = AnonymousUser()
