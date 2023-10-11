from http import HTTPStatus

from django.test import Client, TestCase


class StaticUrlTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)

    def test_coffee_endpoint_code(self):
        response = Client().get("/coffee/")
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)

    def test_coffee_content(self):
        response = Client().get("/coffee/")
        self.assertEqual(response.content, "Я чайник".encode())
