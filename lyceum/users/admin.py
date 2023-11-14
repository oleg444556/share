from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUser
from django.contrib.auth.models import User

import users.models

__all__ = []


class ProfileInline(admin.TabularInline):
    model = users.models.Profile
    can_delete = False
    readonly_fields = (
        users.models.Profile.birthday.field.name,
        users.models.Profile.image.field.name,
        users.models.Profile.coffee_count.field.name,
    )


class UserAdmin(BaseUser):
    inlines = (ProfileInline,)
    readonly_fields = (
        User.first_name.field.name,
        User.last_name.field.name,
        User.email.field.name,
        User.date_joined.field.name,
        User.username.field.name,
        User.last_login.field.name,
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
