from http import HTTPStatus

import django.test
from django.urls import reverse

__all__ = []


class StaticUrlTests(django.test.TestCase):
    # test for catalog items
    def test_catalog_item_list_endpoint(self):
        response = django.test.Client().get(reverse("catalog:item_list"))
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
            msg="Страница не отвечает",
        )

    def test_catalog_item_detail_endpoint_positive(self):
        # test for catalog item details
        for arg in range(0, 10):
            with self.subTest(item_num=arg):
                response = django.test.Client().get(
                    reverse("catalog:item_detail", args=[arg]),
                )
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    msg=f"Страница {arg} не отвечает",
                )

    def test_catalog_item_detail_endpoint_positive_neg(self):
        args = (
            "-1",
            "-0",
            "1.78" "abc",
            "12a",
            "_23",
            "-890",
            "d123",
        )
        for arg in args:
            with self.subTest(item_num=arg):
                response = django.test.Client().get(f"/catalog/{arg}/")
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.NOT_FOUND,
                    msg=f"Страница {arg} отвечает, а не должна",
                )
