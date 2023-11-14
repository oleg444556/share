from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUser
from django.contrib.auth.models import User

import users.models

__all__ = []


class ProfileInline(admin.TabularInline):
    model = users.models.Profile
    can_delete = False


class UserAdmin(BaseUser):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
