import re

from django.conf import settings


class RussianWordsReverseMiddleware:
    _call_count = 0

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        RussianWordsReverseMiddleware._call_count += 1
        response = self._get_response(request)
        allowreverse = settings.ALLOW_REVERSE
        if self._call_count % 10 == 0 and allowreverse:
            text = response.content.decode("utf-8")
            text = self._reverse_all_russian_words(text)
            response.content = text.encode("utf-8")
        return response

    @staticmethod
    def _reverse_all_russian_words(string):
        def reverse_word(match):
            return match.group()[::-1]

        pattern = r"[А-Яа-я]+"
        result = re.sub(pattern, reverse_word, string)
        return result
