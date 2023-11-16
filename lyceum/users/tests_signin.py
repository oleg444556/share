from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
import django.core.exceptions
import django.db
import django.test
from django.urls import reverse
from django.utils import timezone

import users.forms

__all__ = []


class SignInTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем тестового пользователя для проверки авторизации
        cls.test_user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testmail@bk.ru",
            is_active=True,
        )

    def test_signin_positive(self):
        user_data = {
            "username": "test_user_1",
            "email": "testmail@mail.ru",
            "password1": "159874test",
            "password2": "159874test",
        }
        user_form = users.forms.CustomUserCreationForm(user_data)
        self.assertTrue(
            user_form.is_valid(),
            msg="Форма регистрации не валидна",
        )

        users_count = User.objects.count()

        response = django.test.Client().post(
            reverse("users:signup"),
            data=user_data,
            follow=True,
        )

        self.assertEqual(User.objects.count(), users_count + 1)

        self.assertRedirects(response, reverse("users:signup"))

    def test_signin_negative(self):
        user_data = {
            "username": "test_user_2",
            "email": "testmailmail.ru",
            "password1": "159874te",
            "password2": "159874test",
        }
        user_form = users.forms.CustomUserCreationForm(user_data)
        self.assertFalse(
            user_form.is_valid(),
            msg="Форма регистрации валидна",
        )

        users_count = User.objects.count()

        django.test.Client().post(
            reverse("users:signup"),
            data=user_data,
            follow=True,
        )

        self.assertEqual(User.objects.count(), users_count)

    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_activate_signup_user_positive(self):
        user_data = {
            "username": "test_user_1",
            "email": "testmail@mail.ru",
            "password1": "159874test",
            "password2": "159874test",
        }
        user_form = users.forms.CustomUserCreationForm(user_data)
        self.assertTrue(
            user_form.is_valid(),
            msg="Форма регистрации не валидна",
        )

        users_count = User.objects.count()

        django.test.Client().post(
            reverse("users:signup"),
            data=user_data,
            follow=True,
        )

        self.assertEqual(User.objects.count(), users_count + 1)

        user = User.objects.get(username="test_user_1")
        self.assertFalse(user.is_active, msg="Польователь активен")

        django.test.Client().get(
            reverse("users:activate", args=["test_user_1"]),
        )

        user = User.objects.get(username="test_user_1")
        self.assertTrue(user.is_active)

    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_activate_signup_user_negative_time(self):
        user_data = {
            "username": "test_user_1",
            "email": "testmail@mail.ru",
            "password1": "159874test",
            "password2": "159874test",
        }
        user_form = users.forms.CustomUserCreationForm(user_data)
        self.assertTrue(
            user_form.is_valid(),
            msg="Форма регистрации не валидна",
        )

        users_count = User.objects.count()

        django.test.Client().post(
            reverse("users:signup"),
            data=user_data,
            follow=True,
        )

        self.assertEqual(User.objects.count(), users_count + 1)

        user = User.objects.get(username="test_user_1")
        self.assertFalse(user.is_active, msg="Польователь активен")

        now = timezone.now()
        with patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = now + timedelta(hours=12)

            django.test.Client().get(
                reverse("users:activate", args=["test_user_1"]),
            )

            user = User.objects.get(username="test_user_1")
            self.assertFalse(user.is_active)

    def test_able_to_login_mail(self):
        self.assertTrue(
            self.test_user.is_active,
            msg="Тестовый пользователь не активен",
        )

        response = django.test.Client().post(
            reverse("users:login"),
            data={"username": "testmail@bk.ru", "password": "testpassword"},
            follow=True,
        )
        self.assertTrue(response.context["user"].is_authenticated)

    def test_able_to_login_username(self):
        self.assertTrue(
            self.test_user.is_active,
            msg="Тестовый пользователь не активен",
        )

        response = django.test.Client().post(
            reverse("users:login"),
            data={"username": "testuser", "password": "testpassword"},
            follow=True,
        )
        self.assertTrue(response.context["user"].is_authenticated)
