from django.contrib import admin

import feedback.models

__all__ = []


@admin.register(feedback.models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.mail.field.name,
        feedback.models.Feedback.status.field.name,
    )
    list_editable = (feedback.models.Feedback.status.field.name,)
    list_display_links = (feedback.models.Feedback.name.field.name,)
    readonly_fields = (
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.mail.field.name,
        feedback.models.Feedback.text.field.name,
    )

    def save_model(self, request, obj, form, change):
        pk = obj.pk
        if pk and request.user:
            old_feed = feedback.models.Feedback.objects.get(id=pk)
            if obj.status != old_feed.status:
                feedback.models.StatusLog.objects.create(
                    user=request.user,
                    feedback=obj,
                    from_status=old_feed.get_status_display(),
                    to=obj.get_status_display(),
                )
        super().save_model(request, obj, form, change)


@admin.register(feedback.models.StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.StatusLog.user.field.name,
        feedback.models.StatusLog.timestamp.field.name,
        feedback.models.StatusLog.feedback.field.name,
        feedback.models.StatusLog.from_status.field.name,
        feedback.models.StatusLog.to.field.name,
    )
    readonly_fields = (
        feedback.models.StatusLog.user.field.name,
        feedback.models.StatusLog.timestamp.field.name,
        feedback.models.StatusLog.feedback.field.name,
        feedback.models.StatusLog.from_status.field.name,
        feedback.models.StatusLog.to.field.name,
    )
