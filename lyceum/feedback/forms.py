import django.forms

import feedback.models

__all__ = ["FeedbackForm"]


class FeedbackForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
        self.fields["text"].widget.attrs.update(
            {"rows": 2},
        )

    class Meta:
        model = feedback.models.Feedback
        fields = (
            feedback.models.Feedback.mail.field.name,
            feedback.models.Feedback.text.field.name,
        )
        exclude = [feedback.models.Feedback.created_on.field.name]
