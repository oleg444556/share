import django.contrib
import django.core.mail
import django.shortcuts

from feedback import forms
from lyceum import settings

__all__ = []


def feedback(request):
    template = "feedback/feedback.html"
    form = forms.FeedbackForm(request.POST or None)
    context = {"form": form}

    if request.method == "POST":
        if form.is_valid():
            text = form.cleaned_data.get("text")
            mail_to = form.cleaned_data.get("mail")
            django.core.mail.send_mail(
                "Обратная связь",
                text,
                settings.DJANGO_MAIL,
                [mail_to],
                fail_silently=False,
            )
            django.contrib.messages.success(
                request,
                "Письмо было успешно отправлено",
            )
            return django.shortcuts.redirect("feedback:feedback")

    return django.shortcuts.render(request, template, context)
