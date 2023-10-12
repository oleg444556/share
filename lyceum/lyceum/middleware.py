from django.conf import settings


class RussianWordsReverseMiddleware:
    _call_count = 0

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request, *args, **kwargs):
        self._plus_add_count()
        response = self._get_response(request, *args, **kwargs)
        allowreverse = settings.ALLOW_REVERSE
        if self._call_count % 10 == 0 and allowreverse:
            text = response.content.decode("utf-8")
            text = self._reverse_all_russian_words(text)
            response.content = text.encode("utf-8")
        return response

    @classmethod
    def _plus_add_count(cls):
        cls._call_count += 1

    @staticmethod
    def _reverse_all_russian_words(string):
        result = []
        stack = []
        russian_letters_set = set()
        for letter_code in range(ord("а"), ord("я") + 1):
            russian_letters_set.add(chr(letter_code))
        for letter_code in range(ord("А"), ord("Я") + 1):
            russian_letters_set.add(chr(letter_code))
        for letter in string:
            if letter in russian_letters_set:
                stack.append(letter)
            else:
                result += stack[::-1]
                stack.clear()
                result.append(letter)
        result += stack[::-1]
        return "".join(result)
