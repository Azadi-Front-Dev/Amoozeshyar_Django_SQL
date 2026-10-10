
from django.contrib import admin

from .models import Person, Student, Professor, Staff


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "person_id",
        "first_name",
        "last_name",
        "national_id",
        "phone_number",
        "email",
        "is_active",
    )
    list_display_links = ("person_id", "first_name", "last_name")
    search_fields = (
        "first_name",
        "last_name",
        "national_id",
        "phone_number",
        "email",
    )
    list_filter = ("is_active", "gender")
    ordering = ("person_id",)
    list_per_page = 25
    readonly_fields = (
        "person_id",
        "created_at",
        "updated_at",
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "student_number",
        "person",
        "field_of_study",
        "entry_year",
        "status",
    )
    list_display_links = ("student_id", "student_number")
    search_fields = (
        "student_number",
        "person__first_name",
        "person__last_name",
        "person__national_id",
    )
    list_filter = (
        "entry_year",
        "status",
        "field_of_study__education_level",
        "field_of_study",
    )
    ordering = ("student_id",)
    list_per_page = 25
    list_select_related = (
        "person",
        "field_of_study",
        "field_of_study__education_level",
    )
    readonly_fields = ("student_id", "created_at")


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = (
        "professor_id",
        "person",
        "personnel_code",
        "department",
        "academic_rank",
        "status",
    )
    list_display_links = ("professor_id", "person")
    search_fields = (
        "person__first_name",
        "person__last_name",
        "person__national_id",
        "personnel_code",
        "department__name",
    )
    list_filter = (
        "academic_rank",
        "status",
        "department__faculty",
        "department",
    )
    ordering = ("professor_id",)
    list_per_page = 25
    list_select_related = (
        "person",
        "department",
        "department__faculty",
    )
    readonly_fields = ("professor_id", "created_at")


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "staff_id",
        "person",
        "personnel_code",
        "department",
        "position_title",
        "status",
    )
    list_display_links = ("staff_id", "person")
    search_fields = (
        "person__first_name",
        "person__last_name",
        "person__national_id",
        "personnel_code",
        "position_title",
        "department__name",
    )
    list_filter = (
        "status",
        "department__faculty",
        "department",
    )
    ordering = ("staff_id",)
    list_per_page = 25
    list_select_related = (
        "person",
        "department",
        "department__faculty",
    )
    readonly_fields = ("staff_id", "created_at")
