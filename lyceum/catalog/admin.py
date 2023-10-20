from django.contrib import admin, messages
from django.db import IntegrityError, transaction

import catalog.models


@admin.register(catalog.models.Tag)
class TagAdmin(admin.ModelAdmin):
    def remove_default_message(self, request):
        storage = messages.get_messages(request)
        try:
            del storage._queued_messages[-1]
        except KeyError:
            pass

    def save_model(self, request, obj, form, change):
        with transaction.atomic():
            try:
                obj.save()
            except IntegrityError:
                messages.error(
                    request, "Тег с похожим названием уже существует"
                )

    def response_add(self, request, obj, post_url_continue=None):
        response = super().response_add(request, obj, post_url_continue)
        if len(messages.get_messages(request)) > 1:
            self.remove_default_message(request)
        return response

    def response_change(self, request, obj):
        response = super().response_change(request, obj)
        if len(messages.get_messages(request)) > 1:
            self.remove_default_message(request)
        return response


@admin.register(catalog.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    def remove_default_message(self, request):
        storage = messages.get_messages(request)
        try:
            del storage._queued_messages[-1]
        except KeyError:
            pass

    def save_model(self, request, obj, form, change):
        with transaction.atomic():
            try:
                obj.save()
            except IntegrityError:
                messages.error(
                    request, "Категория с похожим названием уже существует"
                )

    def response_add(self, request, obj, post_url_continue=None):
        response = super().response_add(request, obj, post_url_continue)
        if len(messages.get_messages(request)) > 1:
            self.remove_default_message(request)
        return response

    def response_change(self, request, obj):
        response = super().response_change(request, obj)
        if len(messages.get_messages(request)) > 1:
            self.remove_default_message(request)
        return response


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
