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
        fields = (feedback.models.Feedback.text.field.name,)
        exclude = [
            feedback.models.Feedback.created_on.field.name,
            feedback.models.Feedback.status.field.name,
        ]


class FeedbackPersonalForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = feedback.models.FeedbackPersonal
        fields = (
            feedback.models.FeedbackPersonal.name.field.name,
            feedback.models.FeedbackPersonal.mail.field.name,
        )


class MultipleFileInput(django.forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(django.forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return single_file_clean(data, initial)


class FileFieldForm(django.forms.Form):
    file_field = MultipleFileField()
