from django.contrib import admin

import feedback.models

__all__ = []


class PersonalInline(admin.TabularInline):
    model = feedback.models.FeedbackPersonal
    can_delete = False
    readonly_fields = [
        feedback.models.FeedbackPersonal.name.field.name,
        feedback.models.FeedbackPersonal.mail.field.name,
    ]


@admin.register(feedback.models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.display_name,
        feedback.models.Feedback.display_mail,
        feedback.models.Feedback.status.field.name,
    )
    list_editable = (feedback.models.Feedback.status.field.name,)
    list_display_links = (
        feedback.models.Feedback.display_name,
        feedback.models.Feedback.display_mail,
    )
    readonly_fields = (feedback.models.Feedback.text.field.name,)
    inlines = (PersonalInline,)

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
