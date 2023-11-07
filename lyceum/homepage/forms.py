import django.forms

__all__ = []


class EchoForm(django.forms.Form):
    text = django.forms.CharField(
        label="Текстовое поле",
        help_text="Введите какой-либо текст",
        widget=django.forms.Textarea,
    )

    text.widget.attrs.update({"class": "form-control"})
