
from django.contrib import admin

from .models import Enrollment, EnrollmentHistory


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "enrollment_id",
        "student",
        "class_section",
        "status",
        "registered_at",
        "dropped_at",
    )

    list_display_links = ("enrollment_id", "student")

    search_fields = (
        "student__student_number",
        "student__person__first_name",
        "student__person__last_name",
        "student__person__national_id",
        "class_section__section_code",
        "class_section__course_offering__course__title",
        "class_section__course_offering__course__course_code",
    )

    list_filter = (
        "status",
        "class_section__course_offering__semester__academic_year",
        "class_section__course_offering__semester",
    )

    ordering = ("-registered_at",)

    list_select_related = (
        "student",
        "student__person",
        "class_section",
        "class_section__course_offering",
        "class_section__course_offering__course",
        "class_section__course_offering__semester",
    )

    readonly_fields = (
        "enrollment_id",
        "registered_at",
        "dropped_at",
    )

    list_per_page = 25


@admin.register(EnrollmentHistory)
class EnrollmentHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "history_id",
        "enrollment",
        "old_status",
        "new_status",
        "changed_at",
        "reason",
    )

    list_display_links = ("history_id", "enrollment")

    search_fields = (
        "enrollment__student__student_number",
        "enrollment__student__person__first_name",
        "enrollment__student__person__last_name",
        "enrollment__class_section__section_code",
        "reason",
    )

    list_filter = (
        "old_status",
        "new_status",
        "changed_at",
    )

    ordering = ("-changed_at",)

    list_select_related = (
        "enrollment",
        "enrollment__student",
        "enrollment__student__person",
        "enrollment__class_section",
    )

    readonly_fields = (
        "history_id",
        "enrollment",
        "old_status",
        "new_status",
        "changed_at",
        "reason",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
