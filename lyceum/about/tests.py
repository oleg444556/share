from http import HTTPStatus

import django.test
from django.urls import reverse

__all__ = []


class StaticUrlTests(django.test.TestCase):
    def test_about_endpoint(self):
        response = django.test.Client().get(reverse("about:about"))
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
            msg="Страница о проекте не отвечает",
        )
