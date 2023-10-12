from django.conf import settings


class RussianWordsReverseMiddleware:
    _CALL_COUNT = 0

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        self._CALL_COUNT += 1
        response = self._get_response(request)
        allowreverse = getattr(settings, "ALLOW_REVERSE", False)
        if self._CALL_COUNT == 10 and allowreverse:
            text = response.content.decode("utf-8")
            text = self._reverse_all_russian_words(text)
            response.content = text.encode("utf-8")
            self._CALL_COUNT = 0
        return response

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
