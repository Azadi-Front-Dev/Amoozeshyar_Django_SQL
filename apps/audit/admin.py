
from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "audit_log_id",
        "user",
        "action",
        "entity_name",
        "entity_id",
        "ip_address",
        "created_at",
    )

    list_display_links = ("audit_log_id",)

    search_fields = (
        "action",
        "entity_name",
        "entity_id",
        "user__username",
        "ip_address",
    )

    list_filter = (
        "action",
        "entity_name",
        "created_at",
    )

    ordering = ("-created_at",)

    list_select_related = ("user",)

    readonly_fields = (
        "audit_log_id",
        "user",
        "action",
        "entity_name",
        "entity_id",
        "old_values",
        "new_values",
        "ip_address",
        "user_agent",
        "created_at",
    )

    fields = (
        "audit_log_id",
        "user",
        "action",
        "entity_name",
        "entity_id",
        "old_values",
        "new_values",
        "ip_address",
        "user_agent",
        "created_at",
    )

    list_per_page = 50

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
