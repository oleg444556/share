from catalog import views
from django.test import Client, TestCase
from django.urls import reverse


class StaticUrlTests(TestCase):
    # test for catalog items
    def test_catalog_item_list_endpoint(self):
        response = Client().get(reverse(views.item_list))
        self.assertEqual(response.status_code, 200)

    def test_catalog_item_detail_endpoint(self):
        # test for catalog item details
        response = Client().get(reverse(views.item_detail, args=["1"]))
        self.assertEqual(response.status_code, 200)

    def test_re_exp_correct_status_catalog_endpoint(self):
        # test for correct re_path request
        response = Client().get(
            reverse(views.catalog_int_pos_num, args=["100"])
        )
        self.assertEqual(response.status_code, 200)

    def test_re_exp_correct_content_catalog_endpoint(self):
        # test for correct re_path request, for content of response
        response = Client().get(
            reverse(views.catalog_int_pos_num, args=["100"])
        )
        text = response.content.decode("utf-8")
        self.assertEqual(text, "<body>100</body>")

    def test_converter_status_catalog_endpoint(self):
        # test for correct request
        response = Client().get(
            reverse(views.catalog_converter_int_pos, args=["100"])
        )
        self.assertEqual(response.status_code, 200)

    def test_converter_content_catalog_endpoint(self):
        # test for correct converter request, for content of response
        response = Client().get(
            reverse(views.catalog_converter_int_pos, args=["100"])
        )
        text = response.content.decode("utf-8")
        self.assertEqual(text, "<body>100</body>")
