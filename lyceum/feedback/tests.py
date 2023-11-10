import shutil
import tempfile

import django.core.files.uploadedfile
import django.test
from django.urls import reverse

import feedback.forms
import feedback.models


__all__ = []

TEST_DIR = tempfile.mkdtemp()


@django.test.override_settings(MEDIA_ROOT=TEST_DIR)
class FormsTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.text_form = feedback.forms.FeedbackForm()
        cls.name_form = feedback.forms.FeedbackPersonalForm()

    def test_form_label(self):
        label_text = self.text_form.fields["text"].label
        label_mail = self.name_form.fields["mail"].label
        label_name = self.name_form.fields["name"].label

        self.assertEqual(label_text, "Текст письма")
        self.assertEqual(label_mail, "Почта")
        self.assertEqual(label_name, "Имя отправителя")

    def test_form_help_text(self):
        help_text_text = self.text_form.fields["text"].help_text
        help_text_mail = self.name_form.fields["mail"].help_text
        help_text_name = self.name_form.fields["name"].help_text

        self.assertEqual(help_text_text, "Введите текст письма")
        self.assertEqual(help_text_mail, "Введите вашу почту")
        self.assertEqual(help_text_name, "Введите ваше имя (необязательно)")

    def test_form_in_context(self):
        response = django.test.Client().get(reverse("feedback:feedback"))
        context = response.context

        self.assertIn("form_personal", context)
        self.assertIn("form_text", context)
        self.assertIn("form_files", context)

    def test_post_request_form_redirect(self):
        post_data = {
            "mail": "1@mail.ru",
            "text": "example",
            "name": "example",
        }
        form_test = feedback.forms.FeedbackForm(post_data)

        self.assertTrue(
            form_test.is_valid(),
            msg="Форма не проходит валидацию",
        )

        response = django.test.Client().post(
            reverse("feedback:feedback"),
            data=post_data,
            follow=True,
        )

        self.assertRedirects(response, reverse("feedback:feedback"))

    def test_form_errors(self):
        data = {"mail": "qwerty", "text": None}

        form_person = feedback.forms.FeedbackPersonalForm(data)
        form_text = feedback.forms.FeedbackForm(data)

        self.assertFalse(form_text.is_valid())
        self.assertFalse(form_person.is_valid())

        self.assertTrue(form_person.has_error("mail"))
        self.assertTrue(form_text.has_error("text"))

    def test_feedback_create_valid_form(self):
        post_data = {
            "mail": "1@mail.ru",
            "text": "example",
            "name": "example",
        }

        form_text = feedback.forms.FeedbackForm(post_data)
        form_personal = feedback.forms.FeedbackPersonalForm(post_data)

        self.assertTrue(
            form_text.is_valid(),
            msg="Форма текста не проходит валидацию",
        )
        self.assertTrue(
            form_personal.is_valid(),
            msg="Форма личных данных не проходит валидацию",
        )

        feedback_count = feedback.models.Feedback.objects.count()
        django.test.Client().post(
            reverse("feedback:feedback"),
            data=post_data,
            follow=True,
        )

        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            feedback_count + 1,
        )

    def test_feedback_create_unvalid_form(self):
        post_data = {
            "mail": "mail.ru",
            "text": "",
            "name": "example",
        }

        form_test_person = feedback.forms.FeedbackPersonalForm(post_data)
        form_test_text = feedback.forms.FeedbackForm(post_data)

        self.assertFalse(
            form_test_person.is_valid(),
            msg="Форма личных данных проходит валидацию",
        )
        self.assertFalse(
            form_test_text.is_valid(),
            msg="Форма текста проходит валидацию",
        )

        feedback_count = feedback.models.Feedback.objects.count()
        django.test.Client().post(
            reverse("feedback:feedback"),
            data=post_data,
            follow=True,
        )

        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            feedback_count,
        )

    def test_upload_file_feedback(self):
        file_content = b"Test file content"
        uploaded_file = django.core.files.uploadedfile.SimpleUploadedFile(
            "test_file.txt",
            file_content,
        )

        post_data = {
            "mail": "1@mail.ru",
            "text": "example",
            "name": "example",
            "file_field": [uploaded_file],
        }

        form_text = feedback.forms.FeedbackForm(post_data)
        form_personal = feedback.forms.FeedbackPersonalForm(post_data)

        self.assertTrue(
            form_text.is_valid(),
            msg="Форма текста не проходит валидацию",
        )
        self.assertTrue(
            form_personal.is_valid(),
            msg="Форма личных данных не проходит валидацию",
        )

        files_count = feedback.models.FeedbackFiles.objects.count()
        django.test.Client().post(
            reverse("feedback:feedback"),
            data=post_data,
            follow=True,
        )

        self.assertEqual(
            feedback.models.FeedbackFiles.objects.count(),
            files_count + 1,
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEST_DIR, ignore_errors=True)
        super().tearDownClass()
