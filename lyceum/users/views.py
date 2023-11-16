from datetime import timedelta

from django.conf import settings
import django.contrib.auth.decorators
from django.contrib.auth.models import User
import django.contrib.messages
from django.contrib.sites.shortcuts import get_current_site
import django.core.mail
import django.shortcuts
import django.template.loader
from django.urls import reverse
import django.utils.timezone

import users.forms

__all__ = []


def sign_up(request):
    template = "users/signup.html"
    form = users.forms.CustomUserCreationForm(request.POST or None)
    context = {"form": form}
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = settings.DEFAULT_USER_IS_ACTIVE
            user.save()

            if not settings.DEFAULT_USER_IS_ACTIVE:
                current_site = get_current_site(request).domain
                mail_subject = "Активируйте свой аккаунт"
                link = reverse("users:activate", args=[str(user)])
                message = f"Ссылка для активации: http://{current_site}{link}"
                django.core.mail.send_mail(
                    mail_subject,
                    message,
                    settings.DJANGO_MAIL,
                    [user.email],
                )

            django.contrib.messages.success(
                request,
                "Аккаунт был успешно зарегестрирован",
            )
            return django.shortcuts.redirect("users:signup")

    return django.shortcuts.render(request, template, context)


def activate(request, user):
    template = "users/activate.html"
    user = User.objects.get(username=user)
    try:
        if django.utils.timezone.now() - user.date_joined < timedelta(
            hours=12,
        ):
            user.is_active = True
            user.save()
            activate_message = (
                "Поздравляем, вы успешно активировали свой аккаунт"
            )
        else:
            activate_message = "Это трагедия, срок действия ссылки истёк :("
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        activate_message = "Что то пошло не так"

    context = {"activate_message": activate_message}
    return django.shortcuts.render(request, template, context)


def user_list(request):
    template = "users/user_list.html"
    users = User.objects.filter(is_active=True).all()
    context = {"users": users}
    return django.shortcuts.render(request, template, context)


def user_detail(request, pk):
    template = "users/user_detail.html"
    user = django.shortcuts.get_object_or_404(
        User.objects.select_related("profile").only(
            "email",
            "first_name",
            "last_name",
            "profile__birthday",
            "profile__image",
            "profile__coffee_count",
        ),
        id=pk,
    )
    context = {"user": user}
    return django.shortcuts.render(request, template, context)


@django.contrib.auth.decorators.login_required
def profile(request):
    template = "users/profile.html"
    user_form = users.forms.UserChangeForm(
        request.POST or None,
        instance=request.user,
    )
    profile_form = users.forms.ProfileChangeForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user.profile,
    )
    forms = (user_form, profile_form)
    context = {"forms": forms}

    if request.method == "POST":
        if all(form.is_valid() for form in forms):
            user_form.save()
            profile_form.save()

            django.contrib.messages.success(
                request,
                "Ваш профиль успешно обновлен",
            )

            return django.shortcuts.redirect(
                "users:profile",
            )

    return django.shortcuts.render(request, template, context)
