from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

__all__ = []


class StaticUrlTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get(reverse("homepage:home"))
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
            msg="Страница главная не отвечает",
        )

    def test_coffee_endpoint_code(self):
        response = Client().get(reverse("homepage:coffee"))
        self.assertEqual(
            response.status_code,
            HTTPStatus.IM_A_TEAPOT,
            msg="Код страницы coffee неверный",
        )

    def test_coffee_content(self):
        responses = set()
        responses.add(Client().get(reverse("homepage:coffee")).content)
        responses.add(Client().get(reverse("homepage:coffee")).content)
        self.assertIn(
            "Я чайник".encode(),
            responses,
            msg="Контент страницы coffee неверный",
        )
