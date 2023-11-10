import django.contrib
import django.core.mail
import django.shortcuts

from feedback import forms, models
from lyceum import settings

__all__ = []


def feedback(request):
    template = "feedback/feedback.html"
    form_text = forms.FeedbackForm(request.POST or None)
    form_personal = forms.FeedbackPersonalForm(request.POST or None)
    form_files = forms.FileFieldForm(request.POST, request.FILES)
    form = [form_personal, form_text, form_files]
    context = {"forms": form}

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

            for uploaded_file in form_files.cleaned_data["file_field"]:
                models.FeedbackFiles.objects.create(
                    file=uploaded_file,
                    main_feedback=text,
                )

            django.contrib.messages.success(
                request,
                "Письмо было успешно отправлено",
            )
            return django.shortcuts.redirect("feedback:feedback")

    return django.shortcuts.render(request, template, context)
