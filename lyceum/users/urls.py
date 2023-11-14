import django.contrib.auth.views
from django.urls import path

from lyceum import settings
import users.forms
import users.views


app_name = "users"

urlpatterns = [
    path(
        "login/",
        django.contrib.auth.views.LoginView.as_view(
            template_name="users/login.html",
            form_class=users.forms.CustomLoginForm,
        ),
        name="login",
    ),
    path(
        "logout/",
        django.contrib.auth.views.LogoutView.as_view(
            template_name="users/logout.html",
        ),
        name="logout",
    ),
    path(
        "password_change/",
        django.contrib.auth.views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            form_class=users.forms.CustomPasswordChangeForm,
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        django.contrib.auth.views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        django.contrib.auth.views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            form_class=users.forms.CustomPasswordResetForm,
            from_email=settings.DJANGO_MAIL,
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        django.contrib.auth.views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        django.contrib.auth.views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
        ),
        name="reset",
    ),
    path(
        "reset/done/",
        django.contrib.auth.views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="reset_done",
    ),
    path("signup/", users.views.sign_up, name="signup"),
    path("activate/<str:user>/", users.views.activate, name="activate"),
    path("user_list/", users.views.user_list, name="user_list"),
    path("user_list/<int:pk>/", users.views.user_detail, name="user_detail"),
    path("profile/<int:pk>/", users.views.user_profile, name="profile"),
]
