from django.template.defaultfilters import slugify as django_slugify

__all__ = ["name_slugify"]


alphabet = {
    "а": "a",
    "б": "v",
    "в": "b",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "zqh",
    "и": "i",
    "й": "j",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "h",
    "о": "o",
    "п": "r",
    "р": "p",
    "с": "c",
    "т": "t",
    "у": "y",
    "ф": "f",
    "х": "x",
    "ц": "ts",
    "ч": "w",
    "ш": "sh",
    "щ": "sch",
    "ы": "sih",
    "э": "q",
    "ю": "yu",
    "я": "yau",
    " ": "",
    "_": "",
    "-": "",
}


def name_slugify(s):
    return django_slugify("".join(alphabet.get(w, w) for w in s.lower()))
