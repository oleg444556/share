from django.conf import settings
import django.db
import sorl.thumbnail

__all__ = ["Profile"]


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
