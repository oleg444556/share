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

    def test_re_exp_correct_status_catalog_endpoint(self):
        # test for correct re_path request
        response = Client().get("/catalog/re/100/")
        self.assertEqual(response.status_code, 200)

    def test_re_exp_correct_content_catalog_endpoint(self):
        # test for correct re_path request, for content of response
        response = Client().get("/catalog/re/100/")
        text = response.content.decode("utf-8")
        self.assertEqual(text, "<body>100</body>")

    def test_re_exp_incorrect_status_catalog_endpoint(self):
        # test for incorrect re_path request
        response = Client().get("/catalog/re/-1/")
        self.assertEqual(response.status_code, 404)

    def test_converter_status_catalog_endpoint(self):
        # test for correct request
        response = Client().get("/catalog/converter/100/")
        self.assertEqual(response.status_code, 200)

    def test_converter_content_catalog_endpoint(self):
        # test for correct converter request, for content of response
        response = Client().get("/catalog/converter/100/")
        text = response.content.decode("utf-8")
        self.assertEqual(text, "<body>100</body>")

    def test_converter_incorrect_catalog_endpoint(self):
        # test for incorrect converter request
        response = Client().get("/catalog/converter/-100/")
        self.assertEqual(response.status_code, 404)
