
from django.db import models

from apps.education.models import ClassSection
from apps.users.models import Student


class Enrollment(models.Model):
    enrollment_id = models.IntegerField(
        db_column="EnrollmentId",
        primary_key=True,
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.DO_NOTHING,
        db_column="StudentId",
        related_name="enrollments",
    )
    class_section = models.ForeignKey(
        ClassSection,
        on_delete=models.DO_NOTHING,
        db_column="ClassSectionId",
        related_name="enrollments",
    )
    status = models.CharField(
        db_column="Status",
        max_length=20,
        db_collation="Arabic_CI_AS",
    )
    registered_at = models.DateTimeField(
        db_column="RegisteredAt",
    )
    dropped_at = models.DateTimeField(
        db_column="DroppedAt",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "[registration].[Enrollment]"
        unique_together = (("student", "class_section"),)

    def __str__(self):
        return f"Enrollment {self.enrollment_id}"


class EnrollmentHistory(models.Model):
    history_id = models.BigIntegerField(
        db_column="HistoryId",
        primary_key=True,
    )
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.DO_NOTHING,
        db_column="EnrollmentId",
        related_name="history",
    )
    old_status = models.CharField(
        db_column="OldStatus",
        max_length=20,
        db_collation="Arabic_CI_AS",
        blank=True,
        null=True,
    )
    new_status = models.CharField(
        db_column="NewStatus",
        max_length=20,
        db_collation="Arabic_CI_AS",
    )
    changed_at = models.DateTimeField(
        db_column="ChangedAt",
    )
    reason = models.CharField(
        db_column="Reason",
        max_length=300,
        db_collation="Arabic_CI_AS",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "[registration].[EnrollmentHistory]"

    def __str__(self):
        return f"Enrollment history {self.history_id}"

