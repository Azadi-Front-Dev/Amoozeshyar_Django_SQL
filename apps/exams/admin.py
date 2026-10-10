
from django.contrib import admin

from .models import Exam, ExamResult, CourseGrade


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        "exam_id",
        "class_section",
        "exam_type",
        "exam_date",
        "start_time",
        "end_time",
        "room",
        "status",
    )

    list_display_links = ("exam_id", "class_section")

    search_fields = (
        "class_section__section_code",
        "class_section__course_offering__course__title",
        "class_section__course_offering__course__course_code",
    )

    list_filter = (
        "exam_type",
        "exam_date",
        "status",
    )

    ordering = ("exam_date", "start_time")

    list_select_related = (
        "class_section",
        "class_section__course_offering",
        "class_section__course_offering__course",
        "room",
    )

    readonly_fields = (
        "exam_id",
        "created_at",
    )

    list_per_page = 25

    @admin.display(description="برنامه امتحانات")
    def has_add_permission(self, request):
        return super().has_add_permission(request)


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = (
        "exam_result_id",
        "exam",
        "enrollment",
        "score",
        "status",
        "recorded_at",
    )

    list_display_links = ("exam_result_id", "exam")

    search_fields = (
        "exam__class_section__course_offering__course__title",
        "enrollment__student__student_number",
        "enrollment__student__person__first_name",
        "enrollment__student__person__last_name",
    )

    list_filter = (
        "status",
        "exam__exam_type",
        "exam__exam_date",
    )

    ordering = ("-created_at",)

    list_select_related = (
        "exam",
        "exam__class_section",
        "exam__class_section__course_offering",
        "exam__class_section__course_offering__course",
        "enrollment",
        "enrollment__student",
        "enrollment__student__person",
    )

    readonly_fields = (
        "exam_result_id",
        "created_at",
        "recorded_at",
    )

    list_per_page = 25


@admin.register(CourseGrade)
class CourseGradeAdmin(admin.ModelAdmin):
    list_display = (
        "course_grade_id",
        "enrollment",
        "final_score",
        "status",
        "finalized_at",
    )

    list_display_links = ("course_grade_id", "enrollment")

    search_fields = (
        "enrollment__student__student_number",
        "enrollment__student__person__first_name",
        "enrollment__student__person__last_name",
        "enrollment__class_section__course_offering__course__title",
    )

    list_filter = (
        "status",
        "finalized_at",
    )

    ordering = ("-created_at",)

    list_select_related = (
        "enrollment",
        "enrollment__student",
        "enrollment__student__person",
        "enrollment__class_section",
        "enrollment__class_section__course_offering",
        "enrollment__class_section__course_offering__course",
    )

    readonly_fields = (
        "course_grade_id",
        "created_at",
        "finalized_at",
    )

    list_per_page = 25
