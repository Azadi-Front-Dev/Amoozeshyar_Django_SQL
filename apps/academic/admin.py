
from django.contrib import admin

from .models import (
    University,
    Faculty,
    Department,
    EducationLevel,
    FieldOfStudy,
)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = (
        "university_id",
        "name",
        "code",
        "is_active",
        "created_at",
    )
    list_display_links = ("university_id", "name")
    search_fields = ("name", "code")
    list_filter = ("is_active",)
    ordering = ("university_id",)
    readonly_fields = ("university_id", "created_at")


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = (
        "faculty_id",
        "name",
        "code",
        "university",
        "is_active",
        "created_at",
    )
    list_display_links = ("faculty_id", "name")
    search_fields = (
        "name",
        "code",
        "university__name",
    )
    list_filter = (
        "is_active",
        "university",
    )
    ordering = ("faculty_id",)
    readonly_fields = ("faculty_id", "created_at")
    list_select_related = ("university",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "department_id",
        "name",
        "code",
        "faculty",
        "is_active",
        "created_at",
    )
    list_display_links = ("department_id", "name")
    search_fields = (
        "name",
        "code",
        "faculty__name",
        "faculty__university__name",
    )
    list_filter = (
        "is_active",
        "faculty__university",
        "faculty",
    )
    ordering = ("department_id",)
    readonly_fields = ("department_id", "created_at")
    list_select_related = ("faculty", "faculty__university")


@admin.register(EducationLevel)
class EducationLevelAdmin(admin.ModelAdmin):
    list_display = (
        "education_level_id",
        "name",
        "code",
        "is_active",
    )
    list_display_links = ("education_level_id", "name")
    search_fields = ("name", "code")
    list_filter = ("is_active",)
    ordering = ("education_level_id",)
    readonly_fields = ("education_level_id",)


@admin.register(FieldOfStudy)
class FieldOfStudyAdmin(admin.ModelAdmin):
    list_display = (
        "field_of_study_id",
        "name",
        "code",
        "department",
        "education_level",
        "is_active",
        "created_at",
    )
    list_display_links = ("field_of_study_id", "name")
    search_fields = (
        "name",
        "code",
        "department__name",
        "department__faculty__name",
    )
    list_filter = (
        "is_active",
        "education_level",
        "department__faculty",
        "department",
    )
    ordering = ("field_of_study_id",)
    readonly_fields = ("field_of_study_id", "created_at")
    list_select_related = (
        "department",
        "department__faculty",
        "education_level",
    )
