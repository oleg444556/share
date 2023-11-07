import django.test
from django.urls import reverse

import feedback.forms

__all__ = []


class FormsTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = feedback.forms.FeedbackForm()

    def test_form_label(self):
        label_text = self.form.fields["text"].label
        label_mail = self.form.fields["mail"].label

        self.assertEqual(label_text, "Текст письма")
        self.assertEqual(label_mail, "Почта")

    def test_form_help_text(self):
        help_text_text = self.form.fields["text"].help_text
        help_text_mail = self.form.fields["mail"].help_text

        self.assertEqual(help_text_text, "Введите текст письма")
        self.assertEqual(help_text_mail, "Введите вашу почту")

    def test_form_in_context(self):
        response = django.test.Client().get(reverse("feedback:feedback"))
        context = response.context

        self.assertIn("form", context)

    def test_post_request_form_redirect(self):
        post_data = {
            "mail": "1@mail.ru",
            "text": "example",
        }

        response = django.test.Client().post(
            reverse("feedback:feedback"),
            data=post_data,
            follow=True,
        )

        self.assertRedirects(response, reverse("feedback:feedback"))

    def test_form_errors(self):
        data = {"mail": "qwerty", "text": None}

        form = feedback.forms.FeedbackForm(data)
        self.assertFalse(form.is_valid())

        self.assertTrue(form.has_error('mail'))
        self.assertTrue(form.has_error('text'))
