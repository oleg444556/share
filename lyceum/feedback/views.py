import django.contrib
import django.core.mail
import django.shortcuts

from feedback import forms
from lyceum import settings

__all__ = []


def feedback(request):
    template = "feedback/feedback.html"
    form_text = forms.FeedbackForm(request.POST or None)
    form_personal = forms.FeedbackPersonalForm(request.POST or None)
    form_files = forms.FileFieldForm(request.POST or None)
    context = {
        "form_text": form_text,
        "form_personal": form_personal,
        "form_files": form_files,
    }

    if request.method == "POST":
        if (
            form_text.is_valid()
            and form_personal.is_valid()
            and form_files.is_valid()
        ):
            text = form_text.cleaned_data.get("text")
            mail_to = form_personal.cleaned_data.get("mail")
            django.core.mail.send_mail(
                "Обратная связь",
                text,
                settings.DJANGO_MAIL,
                [mail_to],
                fail_silently=False,
            )

            text = form_text.save()
            personal = form_personal.save(commit=False)
            personal.text_feedback = text
            personal.save()

            for uploaded_file in request.FILES.getlist("file_field"):
                form_files.save(feedback=text, file=uploaded_file)

            django.contrib.messages.success(
                request,
                "Письмо было успешно отправлено",
            )
            return django.shortcuts.redirect("feedback:feedback")

    return django.shortcuts.render(request, template, context)
