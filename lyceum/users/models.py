import re
import sys

from django.conf import settings
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import UserManager
import django.core.validators
import django.db
import sorl.thumbnail

__all__ = ["Profile"]


class CustomUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().select_related("profile")

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, email):
        return self.get_queryset().get(email=email)

    @classmethod
    def normalize_email(cls, email):
        email = super().normalize_email(email)

        email = re.sub(r"\+.*@", "@", email)
        email = email.replace("yandex.ru", "ya.ru")
        email = email.lower()
        if "@gmail.com" in email:
            username, domain = email.split("@")
            username = username.replace(".", "")
            return f"{username}@{domain}"
        if "@ya.ru" in email:
            username, domain = email.split("@")
            username = username.replace(".", "")
            return f"{username}@{domain}"

        return email


class Profile(django.db.models.Model):
    def get_avatar_path(self, filename):
        return f"users/{self.user}/{filename}"

    user = django.db.models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        verbose_name="пользователь",
        related_name="profile",
        null=True,
    )
    birthday = django.db.models.DateField(
        "день рождения",
        help_text="День рождения пользователя(необязательно)",
        null=True,
        blank=True,
    )
    image = django.db.models.ImageField(
        "аватарка",
        upload_to=get_avatar_path,
        help_text="Аватар пользователя(необязательно)",
        null=True,
        blank=True,
    )
    coffee_count = django.db.models.PositiveIntegerField(
        "сварено кофе",
        help_text="Количество переходов по /coffee/",
        default=0,
    )
    attempts_count = django.db.models.PositiveIntegerField(
        "попытки входа",
        help_text="Число неудачных попыток входа",
        default=0,
    )
    reactivation_time = django.db.models.DateTimeField(
        "время деактивации аккаунта",
        help_text="Время преодоления порога максимального"
        " числа неудачных попыток войти",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "дополнительное поле"
        verbose_name_plural = "дополнительные поля"

    def __str__(self):
        return self.user.username

    @property
    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "150x150",
            quality=65,
        )


class User(DjangoUser):
    objects = CustomUserManager()
    if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
        DjangoUser._meta.get_field("email")._unique = True

    class Meta:
        proxy = True

    def clean(self):
        self.email = User.objects.normalize_email(self.email)
        if (
            type(self)
            .objects.filter(email=self.email)
            .exclude(id=self.id)
            .count()
            > 0
        ):
            raise django.core.exceptions.ValidationError(
                "Почта уже существует",
            )
        super().clean()

    def save(self, *args, **kwargs):
        self.email = User.objects.normalize_email(self.email)
        super().save(*args, **kwargs)
