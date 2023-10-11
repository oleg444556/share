from django.test import Client, TestCase


class StaticUrlTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)

    def test_coffee_endpoint_code(self):
        response = Client().get("/coffee/")
        self.assertEqual(response.status_code, 418)

    def test_coffee(self):
        response = Client().get("/coffee/")
        self.assertEqual(response.content, "Я чайник".encode())

    def test_coffee_endpoint_content(self):
        response = Client().get("/coffee/")
        self.assertContains(response, "Я чайник", status_code=418)
