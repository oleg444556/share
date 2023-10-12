from django.test import Client, TestCase, override_settings


class RussianWorldsMiddlewareTests(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_allow_reverse_coffee(self):
        client = Client()
        for i in range(10):
            response = client.get("/coffee/")
        self.assertEqual(response.content, "Я кинйач".encode())

    @override_settings(ALLOW_REVERSE=False)
    def test_allow_reverse_false_coffe(self):
        client = Client()
        for i in range(10):
            response = client.get("/coffee/")
        self.assertEqual(response.content, "Я чайник".encode())
