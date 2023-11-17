import re

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
import django.contrib.messages
from django.contrib.sites.shortcuts import get_current_site
import django.core.exceptions
import django.core.mail
from django.urls import reverse
import django.utils.timezone

import users.models

__all__ = ["EmailBackend"]


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = users.models.User
        email_regex = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
        try:
            if re.match(email_regex, username):
                username = user_model.objects.normalize_email(username)
                user = user_model.objects.by_mail(email=username)
            else:
                user = user_model.objects.get(username=username)
        except user_model.DoesNotExist:
            raise django.core.exceptions.ValidationError(
                "Пользователь не найден",
                code="invalid_login",
            )
        else:
            if user.check_password(password) and self.user_can_authenticate(
                user,
            ):
                user.profile.attempts_count = 0
                user.profile.save()
                return user

            if not user.check_password(
                password,
            ) and self.user_can_authenticate(
                user,
            ):
                user.profile.attempts_count += 1
                user.profile.save()
                if user.profile.attempts_count >= settings.MAX_AUTH_ATTEMPTS:
                    user.is_active = False
                    user.profile.reactivation_time = (
                        django.utils.timezone.now()
                    )
                    user.save()

                    current_site = get_current_site(request).domain
                    mail_subject = "Реактивируйте свой аккаунт"
                    link = reverse("users:reactivate", args=[str(user)])
                    message = (
                        f"Ссылка для активации: http://{current_site}{link}"
                    )
                    django.core.mail.send_mail(
                        mail_subject,
                        message,
                        settings.DJANGO_MAIL,
                        [user.email],
                    )

        return None
