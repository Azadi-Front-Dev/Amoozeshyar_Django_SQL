
from django.db import models

from apps.academic.models import Department, FieldOfStudy


class Person(models.Model):
    person_id = models.AutoField(
        db_column="PersonId",
        primary_key=True,
    )
    national_id = models.CharField(
        db_column="NationalId",
        max_length=10,
        unique=True,
        db_collation="Arabic_CI_AS",
    )
    first_name = models.CharField(
        db_column="FirstName",
        max_length=100,
        db_collation="Arabic_CI_AS",
    )
    last_name = models.CharField(
        db_column="LastName",
        max_length=100,
        db_collation="Arabic_CI_AS",
    )
    birth_date = models.DateField(
        db_column="BirthDate",
        blank=True,
        null=True,
    )
    gender = models.CharField(
        db_column="Gender",
        max_length=1,
        db_collation="Arabic_CI_AS",
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        db_column="PhoneNumber",
        max_length=15,
        unique=True,
        db_collation="Arabic_CI_AS",
        blank=True,
        null=True,
    )
    email = models.CharField(
        db_column="Email",
        max_length=254,
        db_collation="Arabic_CI_AS",
        blank=True,
        null=True,
    )
    address = models.CharField(
        db_column="Address",
        max_length=500,
        db_collation="Arabic_CI_AS",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(db_column="IsActive")
    created_at = models.DateTimeField(db_column="CreatedAt")
    updated_at = models.DateTimeField(
        db_column="UpdatedAt",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "[users].[Person]"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    student_id = models.AutoField(
        db_column="StudentId",
        primary_key=True,
    )
    person = models.OneToOneField(
        Person,
        on_delete=models.DO_NOTHING,
        db_column="PersonId",
        related_name="student",
    )
    student_number = models.CharField(
        db_column="StudentNumber",
        max_length=20,
        unique=True,
        db_collation="Arabic_CI_AS",
    )
    field_of_study = models.ForeignKey(
        FieldOfStudy,
        on_delete=models.DO_NOTHING,
        db_column="FieldOfStudyId",
        related_name="students",
    )
    entry_year = models.SmallIntegerField(db_column="EntryYear")
    status = models.CharField(
        db_column="Status",
        max_length=20,
        db_collation="Arabic_CI_AS",
    )
    created_at = models.DateTimeField(db_column="CreatedAt")

    class Meta:
        managed = False
        db_table = "[users].[Student]"

    def __str__(self):
        return self.student_number


class Professor(models.Model):
    professor_id = models.AutoField(
        db_column="ProfessorId",
        primary_key=True,
    )
    person = models.OneToOneField(
        Person,
        on_delete=models.DO_NOTHING,
        db_column="PersonId",
        related_name="professor",
    )
    personnel_code = models.CharField(
        db_column="PersonnelCode",
        max_length=20,
        unique=True,
        db_collation="Arabic_CI_AS",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.DO_NOTHING,
        db_column="DepartmentId",
        related_name="professors",
    )
    academic_rank = models.CharField(
        db_column="AcademicRank",
        max_length=30,
        db_collation="Arabic_CI_AS",
    )
    status = models.CharField(
        db_column="Status",
        max_length=20,
        db_collation="Arabic_CI_AS",
    )
    created_at = models.DateTimeField(db_column="CreatedAt")

    class Meta:
        managed = False
        db_table = "[users].[Professor]"

    def __str__(self):
        return str(self.person)


class Staff(models.Model):
    staff_id = models.AutoField(
        db_column="StaffId",
        primary_key=True,
    )
    person = models.OneToOneField(
        Person,
        on_delete=models.DO_NOTHING,
        db_column="PersonId",
        related_name="staff",
    )
    personnel_code = models.CharField(
        db_column="PersonnelCode",
        max_length=20,
        unique=True,
        db_collation="Arabic_CI_AS",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.DO_NOTHING,
        db_column="DepartmentId",
        related_name="staff_members",
        blank=True,
        null=True,
    )
    position_title = models.CharField(
        db_column="PositionTitle",
        max_length=150,
        db_collation="Arabic_CI_AS",
    )
    status = models.CharField(
        db_column="Status",
        max_length=20,
        db_collation="Arabic_CI_AS",
    )
    created_at = models.DateTimeField(db_column="CreatedAt")

    class Meta:
        managed = False
        db_table = "[users].[Staff]"

    def __str__(self):
        return str(self.person)
