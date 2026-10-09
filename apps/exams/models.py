
from django.db import models

from apps.education.models import Classroom, ClassSection
from apps.registration.models import Enrollment


class Exam(models.Model):
    exam_id = models.IntegerField(
        db_column="ExamId",
        primary_key=True,
    )
    class_section = models.ForeignKey(
        ClassSection,
        on_delete=models.DO_NOTHING,
        db_column="ClassSectionId",
        related_name="exams",
    )
    exam_type = models.CharField(
        db_column="ExamType",
        max_length=20,
        db_collation="Arabic_CI_AS",
    )
    exam_date = models.DateField(
        db_column="ExamDate",
    )
    start_time = models.TimeField(
        db_column="StartTime",
    )
    end_time = models.TimeField(
        db_column="EndTime",
    )
    room = models.ForeignKey(
        Classroom,
        on_delete=models.DO_NOTHING,
        db_column="RoomId",
        related_name="exams",
        blank=True,
        null=True,
    )
    status = models.CharField(
        db_column="Status",
        max_length=20,
        db_collation="Arabic_CI_AS",
    )
    created_at = models.DateTimeField(
        db_column="CreatedAt",
    )

    class Meta:
        managed = False
        db_table = "[exam].[Exam]"

    def __str__(self):
        return f"Exam {self.exam_id}"


class ExamResult(models.Model):
    exam_result_id = models.BigIntegerField(
        db_column="ExamResultId",
        primary_key=True,
    )
    exam = models.ForeignKey(
        Exam,
        on_delete=models.DO_NOTHING,
        db_column="ExamId",
        related_name="results",
    )
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.DO_NOTHING,
        db_column="EnrollmentId",
        related_name="exam_results",
    )
    score = models.DecimalField(
        db_column="Score",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    status = models.CharField(
        db_column="Status",
        max_length=20,
        db_collation="Arabic_CI_AS",
    )
    recorded_at = models.DateTimeField(
        db_column="RecordedAt",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        db_column="CreatedAt",
    )

    class Meta:
        managed = False
        db_table = "[exam].[ExamResult]"
        unique_together = (("exam", "enrollment"),)

    def __str__(self):
        return f"Exam result {self.exam_result_id}"


class CourseGrade(models.Model):
    course_grade_id = models.BigIntegerField(
        db_column="CourseGradeId",
        primary_key=True,
    )
    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.DO_NOTHING,
        db_column="EnrollmentId",
        related_name="course_grade",
    )
    final_score = models.DecimalField(
        db_column="FinalScore",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    status = models.CharField(
        db_column="Status",
        max_length=20,
        db_collation="Arabic_CI_AS",
    )
    finalized_at = models.DateTimeField(
        db_column="FinalizedAt",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        db_column="CreatedAt",
    )

    class Meta:
        managed = False
        db_table = "[exam].[CourseGrade]"

    def __str__(self):
        return f"Course grade {self.course_grade_id}"