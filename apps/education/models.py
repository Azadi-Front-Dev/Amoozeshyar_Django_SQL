
from django.db import models

from apps.academic.models import Department
from apps.users.models import Professor


class AcademicYear(models.Model):
    academic_year_id = models.IntegerField(
        db_column="AcademicYearId",
        primary_key=True,
    )
    title = models.CharField(
        db_column="Title",
        max_length=50,
        unique=True,
        db_collation="Arabic_CI_AS",
    )
    start_date = models.DateField(db_column="StartDate")
    end_date = models.DateField(db_column="EndDate")
    is_active = models.BooleanField(db_column="IsActive")
    created_at = models.DateTimeField(db_column="CreatedAt")

    class Meta:
        managed = False
        db_table = "[education].[AcademicYear]"

    def __str__(self):
        return self.title


class Semester(models.Model):
    semester_id = models.IntegerField(
        db_column="SemesterId",
        primary_key=True,
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.DO_NOTHING,
        db_column="AcademicYearId",
        related_name="semesters",
    )
    title = models.CharField(
        db_column="Title",
        max_length=100,
        db_collation="Arabic_CI_AS",
    )
    semester_type = models.CharField(
        db_column="SemesterType",
        max_length=20,
        db_collation="Arabic_CI_AS",
    )
    start_date = models.DateField(db_column="StartDate")
    end_date = models.DateField(db_column="EndDate")
    is_active = models.BooleanField(db_column="IsActive")

    class Meta:
        managed = False
        db_table = "[education].[Semester]"
        unique_together = (("academic_year", "title"),)

    def __str__(self):
        return f"{self.academic_year.title} - {self.title}"


class Building(models.Model):
    building_id = models.IntegerField(
        db_column="BuildingId",
        primary_key=True,
    )
    name = models.CharField(
        db_column="Name",
        max_length=150,
        unique=True,
        db_collation="Arabic_CI_AS",
    )
    code = models.CharField(
        db_column="Code",
        max_length=20,
        unique=True,
        db_collation="Arabic_CI_AS",
    )
    address = models.CharField(
        db_column="Address",
        max_length=300,
        db_collation="Arabic_CI_AS",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(db_column="IsActive")
    created_at = models.DateTimeField(db_column="CreatedAt")

    class Meta:
        managed = False
        db_table = "[education].[Building]"

    def __str__(self):
        return self.name


class Classroom(models.Model):
    room_id = models.IntegerField(
        db_column="RoomId",
        primary_key=True,
    )
    building = models.ForeignKey(
        Building,
        on_delete=models.DO_NOTHING,
        db_column="BuildingId",
        related_name="classrooms",
    )
    room_number = models.CharField(
        db_column="RoomNumber",
        max_length=20,
        db_collation="Arabic_CI_AS",
    )
    capacity = models.IntegerField(db_column="Capacity")
    room_type = models.CharField(
        db_column="RoomType",
        max_length=30,
        db_collation="Arabic_CI_AS",
    )
    is_active = models.BooleanField(db_column="IsActive")
    created_at = models.DateTimeField(db_column="CreatedAt")
    floor = models.SmallIntegerField(db_column="Floor")

    class Meta:
        managed = False
        db_table = "[education].[ClassRoom]"
        unique_together = (("building", "room_number"),)

    def __str__(self):
        return f"{self.building.name} - {self.room_number}"


class Course(models.Model):
    course_id = models.IntegerField(
        db_column="CourseId",
        primary_key=True,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.DO_NOTHING,
        db_column="DepartmentId",
        related_name="courses",
    )
    course_code = models.IntegerField(
        db_column="CourseCode",
        unique=True,
    )
    title = models.CharField(
        db_column="Title",
        max_length=200,
        db_collation="Arabic_CI_AS",
    )
    units = models.SmallIntegerField(db_column="Units")
    course_type = models.CharField(
        db_column="CourseType",
        max_length=30,
        db_collation="Arabic_CI_AS",
    )
    description = models.CharField(
        db_column="Description",
        max_length=500,
        db_collation="Arabic_CI_AS",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(db_column="IsActive")
    created_at = models.DateTimeField(db_column="CreatedAt")

    class Meta:
        managed = False
        db_table = "[education].[Course]"

    def __str__(self):
        return f"{self.course_code} - {self.title}"


class CourseOffering(models.Model):
    course_offering_id = models.IntegerField(
        db_column="CourseOfferingId",
        primary_key=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.DO_NOTHING,
        db_column="CourseId",
        related_name="offerings",
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.DO_NOTHING,
        db_column="SemesterId",
        related_name="course_offerings",
    )
    capacity = models.IntegerField(db_column="Capacity")
    status = models.CharField(
        db_column="Status",
        max_length=20,
        db_collation="Arabic_CI_AS",
    )
    created_at = models.DateTimeField(db_column="CreatedAt")

    class Meta:
        managed = False
        db_table = "[education].[CourseOffering]"
        unique_together = (("course", "semester"),)

    def __str__(self):
        return f"{self.course.title} - {self.semester.title}"


class ClassSection(models.Model):
    class_section_id = models.IntegerField(
        db_column="ClassSectionId",
        primary_key=True,
    )
    course_offering = models.ForeignKey(
        CourseOffering,
        on_delete=models.DO_NOTHING,
        db_column="CourseOfferingId",
        related_name="sections",
    )
    professor = models.ForeignKey(
        Professor,
        on_delete=models.DO_NOTHING,
        db_column="ProfessorId",
        related_name="class_sections",
    )
    section_code = models.CharField(
        db_column="SectionCode",
        max_length=20,
        db_collation="Arabic_CI_AS",
    )
    capacity = models.IntegerField(db_column="Capacity")
    status = models.CharField(
        db_column="Status",
        max_length=20,
        db_collation="Arabic_CI_AS",
    )
    created_at = models.DateTimeField(db_column="CreatedAt")

    class Meta:
        managed = False
        db_table = "[education].[ClassSection]"
        unique_together = (("course_offering", "section_code"),)

    def __str__(self):
        return f"{self.course_offering} - {self.section_code}"


class ClassSchedule(models.Model):
    schedule_id = models.IntegerField(
        db_column="ScheduleId",
        primary_key=True,
    )
    class_section = models.ForeignKey(
        ClassSection,
        on_delete=models.DO_NOTHING,
        db_column="ClassSectionId",
        related_name="schedules",
    )
    room = models.ForeignKey(
        Classroom,
        on_delete=models.DO_NOTHING,
        db_column="RoomId",
        related_name="schedules",
    )
    day_of_week = models.SmallIntegerField(db_column="DayOfWeek")
    start_time = models.TimeField(db_column="StartTime")
    end_time = models.TimeField(db_column="EndTime")

    class Meta:
        managed = False
        db_table = "[education].[ClassSchedule]"

    def __str__(self):
        return f"{self.class_section} - {self.day_of_week}"


class CoursePrerequisite(models.Model):
    pk = models.CompositePrimaryKey(
        "course",
        "prerequisite_course",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.DO_NOTHING,
        db_column="CourseId",
        related_name="prerequisites",
    )
    prerequisite_course = models.ForeignKey(
        Course,
        on_delete=models.DO_NOTHING,
        db_column="PrerequisiteCourseId",
        related_name="required_for_courses",
    )

    class Meta:
        managed = False
        db_table = "[education].[CoursePrerequisite]"

    def __str__(self):
        return f"{self.course} requires {self.prerequisite_course}"