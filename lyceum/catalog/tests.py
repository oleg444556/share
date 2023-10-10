from django.test import Client, TestCase


class StaticUrlTests(TestCase):
    # test for catalog items
    def test_catalog_item_list_endpoint(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_item_detail_endpoint(self):
        # test for catalog item details
        response = Client().get("/catalog/1/")
        self.assertEqual(response.status_code, 200)
