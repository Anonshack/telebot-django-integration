from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import BotUsers, FeedbackForAdmin


class BotUsersResource(resources.ModelResource):
    class Meta:
        model = BotUsers
        fields = ("id", "user_id", "name", "username", "created_at")
        export_order = ("id", "user_id", "name", "username", "created_at")


@admin.register(BotUsers)
class BotUsersAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = BotUsersResource

    list_display = ("id", "user_id", "name", "username", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user_id", "name", "username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    fieldsets = (
        ("User Information", {
            "fields": ("user_id", "name", "username")
        }),
        ("System Data", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )

class FeedbackResource(resources.ModelResource):
    class Meta:
        model = FeedbackForAdmin
        fields = ("id", "user", "text", "created_at")
        export_order = ("id", "user", "text", "created_at")


@admin.register(FeedbackForAdmin)
class FeedbackForAdminAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = FeedbackResource

    list_display = ("id", "user", "short_text", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("user__username", "user__name", "text")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Feedback Info", {
            "fields": ("user", "text")
        }),
        ("System Info", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )
