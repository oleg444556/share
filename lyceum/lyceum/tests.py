from django.test import Client, modify_settings, TestCase
from django.urls import reverse

__all__ = ["RussianWorldsMiddlewareTests"]


class RussianWorldsMiddlewareTests(TestCase):
    @modify_settings(
        MIDDLEWARE={
            "append": "lyceum.middleware.RussianWordsReverseMiddleware",
        },
    )
    def test_reverse_russian_words_enabled(self):
        contents = {
            Client().get(reverse("homepage:coffee")).content for _ in range(10)
        }
        self.assertIn("Я чайник".encode(), contents)
        self.assertIn("Я кинйач".encode(), contents)

    @modify_settings(
        MIDDLEWARE={
            "remove": "lyceum.middleware.RussianWordsReverseMiddleware",
        },
    )
    def test_reverse_russian_words_disabled(self):
        contents = {
            Client().get(reverse("homepage:coffee")).content for _ in range(10)
        }
        self.assertIn("Я чайник".encode(), contents)
        self.assertNotIn("Я кинйач".encode(), contents)
