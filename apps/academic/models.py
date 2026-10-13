
from django.db import models


class University(models.Model):
    university_id = models.IntegerField(
        db_column="UniversityId",
        primary_key=True,
        verbose_name="شناسه دانشگاه",
    )
    name = models.CharField(
        db_column="Name",
        max_length=200,
        unique=True,
        db_collation="Arabic_CI_AS",
        verbose_name="نام دانشگاه",
    )
    code = models.CharField(
        db_column="Code",
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        db_collation="Arabic_CI_AS",
        verbose_name="کد دانشگاه",
    )
    is_active = models.BooleanField(
        db_column="IsActive",
        verbose_name="وضعیت فعالیت",
    )
    created_at = models.DateTimeField(
        db_column="CreatedAt",
        verbose_name="تاریخ ایجاد",
    )

    class Meta:
        managed = False
        db_table = "[academic].[University]"
        verbose_name = "دانشگاه"
        verbose_name_plural = "دانشگاه‌ها"

    def __str__(self):
        return self.name


class Faculty(models.Model):
    faculty_id = models.IntegerField(
        db_column="FacultyId",
        primary_key=True,
        verbose_name="شناسه دانشکده",
    )
    university = models.ForeignKey(
        University,
        on_delete=models.DO_NOTHING,
        db_column="UniversityId",
        verbose_name="دانشگاه",
    )
    name = models.CharField(
        db_column="Name",
        max_length=200,
        db_collation="Arabic_CI_AS",
        verbose_name="نام دانشکده",
    )
    code = models.CharField(
        db_column="Code",
        max_length=20,
        blank=True,
        null=True,
        db_collation="Arabic_CI_AS",
        verbose_name="کد دانشکده",
    )
    is_active = models.BooleanField(
        db_column="IsActive",
        verbose_name="وضعیت فعالیت",
    )
    created_at = models.DateTimeField(
        db_column="CreatedAt",
        verbose_name="تاریخ ایجاد",
    )

    class Meta:
        managed = False
        db_table = "[academic].[Faculty]"
        verbose_name = "دانشکده"
        verbose_name_plural = "دانشکده‌ها"
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
        verbose_name="شناسه گروه آموزشی",
    )
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.DO_NOTHING,
        db_column="FacultyId",
        verbose_name="دانشکده",
    )
    name = models.CharField(
        db_column="Name",
        max_length=200,
        db_collation="Arabic_CI_AS",
        verbose_name="نام گروه آموزشی",
    )
    code = models.CharField(
        db_column="Code",
        max_length=20,
        blank=True,
        null=True,
        db_collation="Arabic_CI_AS",
        verbose_name="کد گروه آموزشی",
    )
    is_active = models.BooleanField(
        db_column="IsActive",
        verbose_name="وضعیت فعالیت",
    )
    created_at = models.DateTimeField(
        db_column="CreatedAt",
        verbose_name="تاریخ ایجاد",
    )

    class Meta:
        managed = False
        db_table = "[academic].[Department]"
        verbose_name = "گروه آموزشی"
        verbose_name_plural = "گروه‌های آموزشی"
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
        verbose_name="شناسه مقطع تحصیلی",
    )
    name = models.CharField(
        db_column="Name",
        max_length=100,
        unique=True,
        db_collation="Arabic_CI_AS",
        verbose_name="نام مقطع تحصیلی",
    )
    code = models.CharField(
        db_column="Code",
        max_length=20,
        unique=True,
        db_collation="Arabic_CI_AS",
        verbose_name="کد مقطع تحصیلی",
    )
    is_active = models.BooleanField(
        db_column="IsActive",
        verbose_name="وضعیت فعالیت",
    )

    class Meta:
        managed = False
        db_table = "[academic].[EducationLevel]"
        verbose_name = "مقطع تحصیلی"
        verbose_name_plural = "مقاطع تحصیلی"

    def __str__(self):
        return self.name


class FieldOfStudy(models.Model):
    field_of_study_id = models.IntegerField(
        db_column="FieldOfStudyId",
        primary_key=True,
        verbose_name="شناسه رشته تحصیلی",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.DO_NOTHING,
        db_column="DepartmentId",
        verbose_name="گروه آموزشی",
    )
    education_level = models.ForeignKey(
        EducationLevel,
        on_delete=models.DO_NOTHING,
        db_column="EducationLevelId",
        verbose_name="مقطع تحصیلی",
    )
    name = models.CharField(
        db_column="Name",
        max_length=200,
        db_collation="Arabic_CI_AS",
        verbose_name="نام رشته تحصیلی",
    )
    code = models.CharField(
        db_column="Code",
        max_length=20,
        unique=True,
        db_collation="Arabic_CI_AS",
        verbose_name="کد رشته تحصیلی",
    )
    is_active = models.BooleanField(
        db_column="IsActive",
        verbose_name="وضعیت فعالیت",
    )
    created_at = models.DateTimeField(
        db_column="CreatedAt",
        verbose_name="تاریخ ایجاد",
    )

    class Meta:
        managed = False
        db_table = "[academic].[FieldOfStudy]"
        verbose_name = "رشته تحصیلی"
        verbose_name_plural = "رشته‌های تحصیلی"
        unique_together = (
            ("department", "education_level", "name"),
        )

    def __str__(self):
        return self.name
