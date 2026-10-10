
from django.contrib import admin

from .models import (
    AcademicYear,
    Semester,
    Building,
    Classroom,
    Course,
    CourseOffering,
    ClassSection,
    ClassSchedule,
    CoursePrerequisite,
)


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = (
        "academic_year_id",
        "title",
        "start_date",
        "end_date",
        "is_active",
    )
    search_fields = ("title",)
    list_filter = ("is_active",)
    ordering = ("-start_date",)
    readonly_fields = ("academic_year_id", "created_at")


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = (
        "semester_id",
        "title",
        "academic_year",
        "semester_type",
        "start_date",
        "end_date",
        "is_active",
    )
    search_fields = ("title", "academic_year__title")
    list_filter = ("academic_year", "semester_type", "is_active")
    ordering = ("-start_date",)
    list_select_related = ("academic_year",)
    readonly_fields = ("semester_id",)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = (
        "building_id",
        "name",
        "code",
        "address",
        "is_active",
    )
    search_fields = ("name", "code")
    list_filter = ("is_active",)
    ordering = ("building_id",)
    readonly_fields = ("building_id", "created_at")


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = (
        "room_id",
        "room_number",
        "building",
        "floor",
        "room_type",
        "capacity",
        "is_active",
    )
    search_fields = ("room_number", "building__name")
    list_filter = ("building", "floor", "room_type", "is_active")
    ordering = ("building", "room_number")
    list_select_related = ("building",)
    readonly_fields = ("room_id", "created_at")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "course_id",
        "course_code",
        "title",
        "department",
        "units",
        "course_type",
        "is_active",
    )
    list_display_links = ("course_id", "title")
    search_fields = (
        "title",
        "course_code",
        "department__name",
    )
    list_filter = (
        "department__faculty",
        "department",
        "course_type",
        "units",
        "is_active",
    )
    ordering = ("course_code",)
    list_select_related = ("department",)
    readonly_fields = ("course_id", "created_at")


@admin.register(CourseOffering)
class CourseOfferingAdmin(admin.ModelAdmin):
    list_display = (
        "course_offering_id",
        "course",
        "semester",
        "capacity",
        "status",
        "created_at",
    )
    search_fields = (
        "course__title",
        "course__course_code",
        "semester__title",
    )
    list_filter = (
        "semester__academic_year",
        "semester",
        "status",
    )
    ordering = ("-course_offering_id",)
    list_select_related = ("course", "semester", "semester__academic_year")
    readonly_fields = ("course_offering_id", "created_at")


@admin.register(ClassSection)
class ClassSectionAdmin(admin.ModelAdmin):
    list_display = (
        "class_section_id",
        "course_offering",
        "section_code",
        "professor",
        "capacity",
        "status",
    )
    search_fields = (
        "section_code",
        "course_offering__course__title",
        "professor__person__first_name",
        "professor__person__last_name",
        "professor__personnel_code",
    )
    list_filter = (
        "status",
        "course_offering__semester",
        "professor__department",
    )
    ordering = ("class_section_id",)
    list_select_related = (
        "course_offering",
        "course_offering__course",
        "course_offering__semester",
        "professor",
        "professor__person",
    )
    readonly_fields = ("class_section_id", "created_at")


@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "schedule_id",
        "class_section",
        "room",
        "day_of_week",
        "start_time",
        "end_time",
    )
    search_fields = (
        "class_section__section_code",
        "class_section__course_offering__course__title",
        "room__room_number",
        "room__building__name",
    )
    list_filter = ("day_of_week", "room__building")
    ordering = ("day_of_week", "start_time")
    list_select_related = (
        "class_section",
        "class_section__course_offering",
        "class_section__course_offering__course",
        "room",
        "room__building",
    )
    readonly_fields = ("schedule_id",)


