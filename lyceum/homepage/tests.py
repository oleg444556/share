from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from homepage import views


class StaticUrlTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get(reverse(views.home))
        self.assertEqual(response.status_code, 200)

    def test_coffee_endpoint_code(self):
        response = Client().get("/coffee/")
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)

    def test_coffee_content(self):
        responses = set()
        responses.add(Client().get("/coffee/").content)
        responses.add(Client().get("/coffee/").content)
        self.assertIn("Я чайник".encode(), responses)
