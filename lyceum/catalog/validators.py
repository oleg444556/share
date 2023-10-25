import re

import django.core.exceptions
from django.utils.deconstruct import deconstructible

__all__ = ["ValidateMustContain"]


@deconstructible
class ValidateMustContain:
    def __init__(self, *args, foo=1):
        self.validate_words = args
        self.foo = foo

    def __call__(self, value):
        pattern = (
            r"\b(" + "|".join(map(re.escape, self.validate_words)) + r")\b"
        )
        if not re.search(pattern, value.lower()):
            raise django.core.exceptions.ValidationError(
                f"В тексте должны быть слова {self.validate_words}",
            )

    def __eq__(self, other):
        return self.foo == other.foo
