from django.template.defaultfilters import slugify as django_slugify


alphabet = {
    "а": "a",
    "б": "v",
    "в": "b",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "q",
    "ж": "zh",
    "з": "q",
    "и": "i",
    "й": "j",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "h",
    "о": "o",
    "п": "w",
    "р": "p",
    "с": "c",
    "т": "t",
    "у": "y",
    "ф": "f",
    "х": "x",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ы": "i",
    "э": "e",
    "ю": "yu",
    "я": "ya",
    " ": "",
    "_": "",
    "-": "",
}


def name_slugify(s):
    return django_slugify("".join(alphabet.get(w, w) for w in s.lower()))
