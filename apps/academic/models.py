from django.db import models


class University(models.Model):
    university_id = models.IntegerField(
        db_column="UniversityId",
        primary_key=True,
    )
    name = models.CharField(
        db_column="Name",
        max_length=200,
        unique=True,
        db_collation="Arabic_CI_AS",
    )
    code = models.CharField(
        db_column="Code",
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        db_collation="Arabic_CI_AS",
    )
    is_active = models.BooleanField(db_column="IsActive")
    created_at = models.DateTimeField(db_column="CreatedAt")

    class Meta:
        managed = False
        db_table = "[academic].[University]"

    def __str__(self):
        return self.name


class Faculty(models.Model):
    faculty_id = models.IntegerField(
        db_column="FacultyId",
        primary_key=True,
    )
    university = models.ForeignKey(
        University,
        on_delete=models.DO_NOTHING,
        db_column="UniversityId",
    )
    name = models.CharField(
        db_column="Name",
        max_length=200,
        db_collation="Arabic_CI_AS",
    )
    code = models.CharField(
        db_column="Code",
        max_length=20,
        blank=True,
        null=True,
        db_collation="Arabic_CI_AS",
    )
    is_active = models.BooleanField(db_column="IsActive")
    created_at = models.DateTimeField(db_column="CreatedAt")

    class Meta:
        managed = False
        db_table = "[academic].[Faculty]"
        unique_together = (
            ("university", "code"),
            ("university", "name"),
        )

    def __str__(self):
        return self.name


class Department(models.Model):
    department_id = models.IntegerField(
        db_column="DepartmentId",
        primary_key=True,
    )
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.DO_NOTHING,
        db_column="FacultyId",
    )
    name = models.CharField(
        db_column="Name",
        max_length=200,
        db_collation="Arabic_CI_AS",
    )
    code = models.CharField(
        db_column="Code",
        max_length=20,
        blank=True,
        null=True,
        db_collation="Arabic_CI_AS",
    )
    is_active = models.BooleanField(db_column="IsActive")
    created_at = models.DateTimeField(db_column="CreatedAt")

    class Meta:
        managed = False
        db_table = "[academic].[Department]"
        unique_together = (
            ("faculty", "code"),
            ("faculty", "name"),
        )

    def __str__(self):
        return self.name


class EducationLevel(models.Model):
    education_level_id = models.IntegerField(
        db_column="EducationLevelId",
        primary_key=True,
    )
    name = models.CharField(
        db_column="Name",
        max_length=100,
        unique=True,
        db_collation="Arabic_CI_AS",
    )
    code = models.CharField(
        db_column="Code",
        max_length=20,
        unique=True,
        db_collation="Arabic_CI_AS",
    )
    is_active = models.BooleanField(db_column="IsActive")

    class Meta:
        managed = False
        db_table = "[academic].[EducationLevel]"

    def __str__(self):
        return self.name


class FieldOfStudy(models.Model):
    field_of_study_id = models.IntegerField(
        db_column="FieldOfStudyId",
        primary_key=True,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.DO_NOTHING,
        db_column="DepartmentId",
    )
    education_level = models.ForeignKey(
        EducationLevel,
        on_delete=models.DO_NOTHING,
        db_column="EducationLevelId",
    )
    name = models.CharField(
        db_column="Name",
        max_length=200,
        db_collation="Arabic_CI_AS",
    )
    code = models.CharField(
        db_column="Code",
        max_length=20,
        unique=True,
        db_collation="Arabic_CI_AS",
    )
    is_active = models.BooleanField(db_column="IsActive")
    created_at = models.DateTimeField(db_column="CreatedAt")

    class Meta:
        managed = False
        db_table = "[academic].[FieldOfStudy]"
        unique_together = (
            ("department", "education_level", "name"),
        )

    def __str__(self):
        return self.name
