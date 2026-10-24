from rest_framework import serializers

from apps.registration.models import Enrollment
from .models import CourseGrade, ExamResult


class ExamResultSerializer(serializers.ModelSerializer):
    exam_id = serializers.IntegerField(read_only=True)

    exam_type = serializers.CharField(
        source="exam.exam_type",
        read_only=True,
    )
    exam_date = serializers.DateField(
        source="exam.exam_date",
        read_only=True,
    )

    class Meta:
        model = ExamResult
        fields = [
            "exam_id",
            "exam_type",
            "exam_date",
            "score",
            "status",
            "recorded_at",
        ]


class StudentGradeSerializer(serializers.ModelSerializer):
    enrollment_status = serializers.CharField(
        source="status",
        read_only=True,
    )

    course_title = serializers.CharField(
        source="class_section.course_offering.course.title",
        read_only=True,
    )
    course_code = serializers.IntegerField(
        source="class_section.course_offering.course.course_code",
        read_only=True,
    )
    units = serializers.IntegerField(
        source="class_section.course_offering.course.units",
        read_only=True,
    )
    section_code = serializers.CharField(
        source="class_section.section_code",
        read_only=True,
    )
    semester_title = serializers.CharField(
        source="class_section.course_offering.semester.title",
        read_only=True,
    )
    academic_year = serializers.CharField(
        source="class_section.course_offering.semester.academic_year.title",
        read_only=True,
    )

    final_score = serializers.SerializerMethodField()
    grade_status = serializers.SerializerMethodField()
    finalized_at = serializers.SerializerMethodField()

    exams = ExamResultSerializer(
        source="exam_results",
        many=True,
        read_only=True,
    )

    def get_final_score(self, obj):
        try:
            return obj.course_grade.final_score
        except CourseGrade.DoesNotExist:
            return None

    def get_grade_status(self, obj):
        try:
            return obj.course_grade.status
        except CourseGrade.DoesNotExist:
            return None

    def get_finalized_at(self, obj):
        try:
            return obj.course_grade.finalized_at
        except CourseGrade.DoesNotExist:
            return None

    class Meta:
        model = Enrollment
        fields = [
            "enrollment_id",
            "enrollment_status",
            "course_title",
            "course_code",
            "units",
            "section_code",
            "semester_title",
            "academic_year",
            "final_score",
            "grade_status",
            "finalized_at",
            "exams",
        ]
