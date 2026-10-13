
from rest_framework import serializers

from apps.academic.models import (
    University,
    Faculty,
    Department,
    EducationLevel,
    FieldOfStudy,
)


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = (
            "university_id",
            "name",
            "code",
            "is_active",
            "created_at",
        )
        read_only_fields = fields


class FacultySerializer(serializers.ModelSerializer):
    university_name = serializers.CharField(
        source="university.name",
        read_only=True,
    )

    class Meta:
        model = Faculty
        fields = (
            "faculty_id",
            "university",
            "university_name",
            "name",
            "code",
            "is_active",
            "created_at",
        )
        read_only_fields = fields


class DepartmentSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(
        source="faculty.name",
        read_only=True,
    )
    university_name = serializers.CharField(
        source="faculty.university.name",
        read_only=True,
    )

    class Meta:
        model = Department
        fields = (
            "department_id",
            "faculty",
            "faculty_name",
            "university_name",
            "name",
            "code",
            "is_active",
            "created_at",
        )
        read_only_fields = fields


class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = (
            "education_level_id",
            "name",
            "code",
            "is_active",
        )
        read_only_fields = fields


class FieldOfStudySerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source="department.name",
        read_only=True,
    )
    faculty_name = serializers.CharField(
        source="department.faculty.name",
        read_only=True,
    )
    university_name = serializers.CharField(
        source="department.faculty.university.name",
        read_only=True,
    )
    education_level_name = serializers.CharField(
        source="education_level.name",
        read_only=True,
    )

    class Meta:
        model = FieldOfStudy
        fields = (
            "field_of_study_id",
            "name",
            "code",
            "department",
            "department_name",
            "faculty_name",
            "university_name",
            "education_level",
            "education_level_name",
            "is_active",
            "created_at",
        )
        read_only_fields = fields


class UniversityQuerySerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=False)
    search = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=200,
    )
    ordering = serializers.ChoiceField(
        required=False,
        choices=(
            "university_id",
            "-university_id",
            "name",
            "-name",
            "code",
            "-code",
            "created_at",
            "-created_at",
        ),
    )


class AcademicQuerySerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=False)
    search = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=200,
    )
    ordering = serializers.ChoiceField(
        required=False,
        choices=(
            "name",
            "-name",
            "code",
            "-code",
            "created_at",
            "-created_at",
        ),
    )
    university = serializers.IntegerField(required=False, min_value=1)
    faculty = serializers.IntegerField(required=False, min_value=1)
    department = serializers.IntegerField(required=False, min_value=1)
    education_level = serializers.IntegerField(required=False, min_value=1)
