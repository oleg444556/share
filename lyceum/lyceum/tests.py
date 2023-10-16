from django.conf import settings
from django.test import Client, override_settings, TestCase
from django.urls import reverse
from homepage import views


class RussianWorldsMiddlewareTests(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_russian_words_enabled(self):
        self.assertEqual(settings.ALLOW_REVERSE, True)
        contents = {
            Client().get(reverse(views.coffee_endpoint)).content
            for _ in range(10)
        }
        self.assertIn("Я чайник".encode(), contents)
        self.assertIn("Я кинйач".encode(), contents)

    def test_reverse_russian_words_enabled_default(self):
        contents = {
            Client().get(reverse(views.coffee_endpoint)).content
            for _ in range(10)
        }
        self.assertIn("Я чайник".encode(), contents)
        self.assertIn("Я кинйач".encode(), contents)

    @override_settings(ALLOW_REVERSE=False)
    def test_reverse_russian_words_disabled(self):
        contents = {
            Client().get(reverse(views.coffee_endpoint)).content
            for _ in range(10)
        }
        self.assertIn("Я чайник".encode(), contents)
        self.assertNotIn("Я кинйач".encode(), contents)
