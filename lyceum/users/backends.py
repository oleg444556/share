from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.sites.shortcuts import get_current_site
import django.core.mail
from django.urls import reverse
from django.utils.timezone import now

import users.models

__all__ = ["EmailBackend"]


class EmailBackend(ModelBackend):
    def attemts_count_logic(self, user, password, request):
        if not user.check_password(
            password,
        ) and self.user_can_authenticate(
            user,
        ):
            user.profile.attempts_count += 1
            user.profile.save()
            if user.profile.attempts_count >= settings.MAX_AUTH_ATTEMPTS:
                user.is_active = False
                user.profile.reactivation_time = now()
                user.save()

                current_site = get_current_site(request).domain
                mail_subject = "Реактивируйте свой аккаунт"
                link = reverse("users:reactivate", args=[str(user)])
                message = f"Ссылка для активации: http://{current_site}{link}"
                django.core.mail.send_mail(
                    mail_subject,
                    message,
                    settings.DJANGO_MAIL,
                    [user.email],
                )

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = users.models.User
        try:
            username = user_model.objects.normalize_email(username)
            user = user_model.objects.by_mail(username)
        except user_model.DoesNotExist:
            try:
                user = user_model.objects.get(username=username)
                self.attemts_count_logic(user, password, request)
            except user_model.DoesNotExist:
                return None
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(
                user,
            ):
                user.profile.attempts_count = 0
                user.profile.save()
                return user
            self.attemts_count_logic(user, password, request)
        return None

    def get_user(self, user_id):
        user_model = users.models.User
        try:
            user = user_model.objects.get(id=user_id)
            return user
        except user_model.DoesNotExist:
            return None


class UserBackend(ModelBackend):
    def authenticate(self, request, username, password, **kwargs):
        user_model = users.models.User
        result = super().authenticate(request, username, password, **kwargs)
        if result:
            user = user_model.objects.get(username=username)
            user.profile.attempts_count = 0
            user.profile.save()
        return result
