from django.conf import settings
from django.test import Client, override_settings, TestCase
from django.urls import reverse

__all__ = ["RussianWorldsMiddlewareTests"]


class RussianWorldsMiddlewareTests(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_russian_words_enabled(self):
        self.assertEqual(settings.ALLOW_REVERSE, True)
        contents = {
            Client().get(reverse("homepage:coffee")).content for _ in range(10)
        }
        self.assertIn("Я чайник".encode(), contents)
        self.assertIn("Я кинйач".encode(), contents)

    @override_settings(ALLOW_REVERSE=False)
    def test_reverse_russian_words_disabled(self):
        contents = {
            Client().get(reverse("homepage:coffee")).content for _ in range(10)
        }
        self.assertIn("Я чайник".encode(), contents)
        self.assertNotIn("Я кинйач".encode(), contents)
