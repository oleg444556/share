import django.contrib.auth.forms
import django.forms

import users.models

__all__ = []


class CustomLoginForm(django.contrib.auth.forms.AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class CustomPasswordChangeForm(django.contrib.auth.forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class CustomPasswordResetForm(django.contrib.auth.forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class CustomPasswordResetConfirmForm(
    django.contrib.auth.forms.SetPasswordForm,
):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class CustomUserCreationForm(django.contrib.auth.forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
        self.fields["email"].required = True

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = users.models.User
        fields = (
            users.models.User.username.field.name,
            users.models.User.email.field.name,
        )


class ProfileChangeForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
        self.fields["coffee_count"].disabled = True

    class Meta:
        model = users.models.Profile
        fields = (
            users.models.Profile.birthday.field.name,
            users.models.Profile.image.field.name,
            users.models.Profile.coffee_count.field.name,
        )


class UserChangeForm(django.contrib.auth.forms.UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
        self.fields["email"].required = True

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = users.models.User
        fields = (
            users.models.User.first_name.field.name,
            users.models.User.last_name.field.name,
            users.models.User.email.field.name,
        )
        help_texts = {
            users.models.User.email.field.name: "Ваша почта",
        }
