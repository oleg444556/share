from django.test import Client, TestCase


class StaticUrlTests(TestCase):
    def test_about_endpoint(self):
        response = Client().get("/about/")
        self.assertEqual(response.status_code, 200)
