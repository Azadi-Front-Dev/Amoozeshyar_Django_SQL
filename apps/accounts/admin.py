
from django.contrib import admin

from .models import Role, UserAccount


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = (
        "role_id",
        "name",
        "display_name",
        "is_active",
        "created_at",
    )
    list_display_links = ("role_id", "display_name")
    search_fields = ("name", "display_name")
    list_filter = ("is_active",)
    ordering = ("role_id",)
    readonly_fields = (
        "role_id",
        "created_at",
    )


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "username",
        "person",
        "is_active",
        "is_locked",
        "last_login_at",
    )
    list_display_links = (
        "user_id",
        "username",
    )
    search_fields = (
        "username",
    )
    list_filter = (
        "is_active",
        "is_locked",
    )
    ordering = ("user_id",)
    exclude = ("password_hash",)
    readonly_fields = (
        "user_id",
        "person",
        "last_login_at",
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
