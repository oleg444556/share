import re

from django.contrib.auth.middleware import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser

import users.models


__all__ = ["RussianWordsReverseMiddleware"]


class RussianWordsReverseMiddleware:
    _call_count = 0

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        RussianWordsReverseMiddleware._call_count += 1
        response = self._get_response(request)
        if self._call_count % 10 == 0:
            text = response.content.decode("utf-8")
            text = self._reverse_all_russian_words(text)
            response.content = text.encode("utf-8")
        return response

    @staticmethod
    def _reverse_all_russian_words(string):
        def reverse_word(match):
            return match.group()[::-1]

        pattern = r"\b[А-Яа-яЁё]+\b"
        return re.sub(pattern, reverse_word, string)


class CustomUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            request.user = users.models.User.objects.get(id=request.user.id)
        else:
            request.user = AnonymousUser()
