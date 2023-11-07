import django.forms

import feedback.models

__all__ = ["FeedbackForm"]


class FeedbackForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs.update(
            {"class": "form-control", "rows": 2},
        )
        self.fields["mail"].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = feedback.models.Feedback
        fields = (
            feedback.models.Feedback.mail.field.name,
            feedback.models.Feedback.text.field.name,
        )
