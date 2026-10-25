from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone

from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsStudent
from apps.education.models import (
    ClassSection,
    ClassSchedule,
    CoursePrerequisite,
)
from apps.exams.models import CourseGrade
from apps.registration.models import (
    Enrollment,
    EnrollmentPeriod,
)
from apps.registration.serializers import (
    AvailableCourseSerializer,
    EnrollRequestSerializer,
)
from apps.users.models import Student


def get_student_for_user(user):
    """دریافت پروفایل دانشجو متصل به کاربر فعلی."""
    try:
        return Student.objects.get(person=user.person)
    except (Student.DoesNotExist, AttributeError):
        return None


class AvailableCoursesView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        now = timezone.now()

        active_period = (
            EnrollmentPeriod.objects
            .filter(
                is_open=True,
                start_at__lte=now,
                end_at__gte=now,
                semester__is_active=True,
            )
            .select_related("semester")
            .first()
        )

        if active_period is None:
            return Response(
                {
                    "enrollment_open": False,
                    "message": "در حال حاضر بازه انتخاب واحد فعالی وجود ندارد.",
                    "results": [],
                },
                status=status.HTTP_200_OK,
            )

        sections = (
            ClassSection.objects
            .filter(
                status="OPEN",
                course_offering__status="OPEN",
                course_offering__semester=active_period.semester,
                course_offering__course__is_active=True,
            )
            .annotate(
                enrolled_count=Count(
                    "enrollments",
                    filter=Q(enrollments__status="ENROLLED"),
                )
            )
            .select_related(
                "course_offering__course",
                "course_offering__semester",
                "professor__person",
            )
            .prefetch_related("schedules")
            .order_by(
                "course_offering__course__title",
                "section_code",
            )
        )

        serializer = AvailableCourseSerializer(
            sections,
            many=True,
        )

        return Response(
            {
                "enrollment_open": True,
                "semester": active_period.semester.title,
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class EnrollStudentView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    @extend_schema(
        request=EnrollRequestSerializer,
        responses={201: EnrollRequestSerializer},
    )
    def post(self, request):
        serializer = EnrollRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        section_id = serializer.validated_data["class_section_id"]
        now = timezone.now()

        def error(message, code=status.HTTP_400_BAD_REQUEST):
            return Response(
                {
                    "success": False,
                    "message": message,
                },
                status=code,
            )

        with transaction.atomic():
            # شناسایی دانشجو
            try:
                student = (
                    Student.objects
                    .select_for_update()
                    .get(person=request.user.person)
                )
            except (Student.DoesNotExist, AttributeError):
                return error(
                    "پروفایل دانشجویی برای حساب شما پیدا نشد.",
                    status.HTTP_403_FORBIDDEN,
                )

            # بررسی بازه فعال انتخاب واحد
            period = (
                EnrollmentPeriod.objects
                .select_related("semester")
                .filter(
                    is_open=True,
                    start_at__lte=now,
                    end_at__gte=now,
                    semester__is_active=True,
                )
                .order_by("-start_at")
                .first()
            )

            if period is None:
                return error(
                    "در حال حاضر انتخاب واحد فعال نیست."
                )

            # دریافت گروه درسی و اطلاعات استاد
            try:
                section = (
                    ClassSection.objects
                    .select_for_update()
                    .select_related(
                        "course_offering__course",
                        "course_offering__semester",
                        "professor__person",
                    )
                    .get(pk=section_id)
                )
            except ClassSection.DoesNotExist:
                return error("گروه درسی موردنظر پیدا نشد.")

            offering = section.course_offering
            course = offering.course

            # استخراج نام استاد
            professor_name = "نامشخص"

            if section.professor and section.professor.person:
                person = section.professor.person

                professor_name = (
                                     f"{person.first_name or ''} "
                                     f"{person.last_name or ''}"
                                 ).strip() or "نامشخص"

            if offering.semester_id != period.semester_id:
                return error(
                    "این گروه متعلق به نیمسال فعال انتخاب واحد نیست."
                )

            if section.status != "OPEN":
                return error(
                    "این گروه در حال حاضر برای انتخاب واحد باز نیست."
                )

            if offering.status != "OPEN":
                return error(
                    "ارائه این درس در حال حاضر امکان‌پذیر نیست."
                )

            if not course.is_active:
                return error("این درس غیرفعال است.")

            # بررسی سابقه ثبت‌نام در همین گروه
            previous = (
                Enrollment.objects
                .select_for_update()
                .filter(
                    student=student,
                    class_section=section,
                )
                .first()
            )

            if previous:
                if previous.status == "ENROLLED":
                    return error(
                        "این گروه را قبلاً انتخاب کرده‌اید."
                    )

                if previous.status == "DROPPED":
                    # بررسی ظرفیت پیش از فعال‌سازی مجدد
                    enrolled_count = Enrollment.objects.filter(
                        class_section=section,
                        status="ENROLLED",
                    ).count()

                    if enrolled_count >= section.capacity:
                        return error(
                            "ظرفیت این گروه تکمیل شده است."
                        )

                    # فعال‌سازی مجدد همان رکورد قبلی
                    previous.status = "ENROLLED"
                    previous.registered_at = now
                    previous.dropped_at = None
                    previous.save(
                        update_fields=[
                            "status",
                            "registered_at",
                            "dropped_at",
                        ]
                    )

                    return Response(
                        {
                            "success": True,
                            "message": "انتخاب مجدد درس با موفقیت انجام شد.",
                            "class_section_id": section.pk,
                            "course_title": course.title,
                            "section_code": section.section_code,
                            "professor_name": professor_name,
                        },
                        status=status.HTTP_200_OK,
                    )

                return error(
                    "وضعیت سابقه ثبت‌نام مشخص نیست؛ با آموزش تماس بگیرید."
                )

            # ثبت‌نام‌های فعال دانشجو در نیمسال فعلی
            current_enrollments = list(
                Enrollment.objects
                .filter(
                    student=student,
                    status="ENROLLED",
                    class_section__course_offering__semester=period.semester,
                )
                .select_related(
                    "class_section__course_offering__course"
                )
            )

            # جلوگیری از انتخاب یک درس در دو گروه
            for enrollment in current_enrollments:
                existing_course_id = (
                    enrollment.class_section
                    .course_offering.course_id
                )

                if existing_course_id == course.course_id:
                    return error(
                        "این درس را قبلاً در همین نیمسال انتخاب کرده‌اید."
                    )

            # بررسی پیش‌نیازها
            prerequisite_ids = set(
                CoursePrerequisite.objects
                .filter(course=course)
                .values_list(
                    "prerequisite_course_id",
                    flat=True,
                )
            )

            passed_course_ids = set(
                CourseGrade.objects
                .filter(
                    enrollment__student=student,
                    status="PASSED",
                )
                .values_list(
                    "enrollment__class_section"
                    "__course_offering__course_id",
                    flat=True,
                )
            )

            missing_ids = prerequisite_ids - passed_course_ids

            if missing_ids:
                missing_courses = list(
                    CoursePrerequisite.objects
                    .filter(
                        course=course,
                        prerequisite_course_id__in=missing_ids,
                    )
                    .values_list(
                        "prerequisite_course__title",
                        flat=True,
                    )
                )

                return error(
                    "ابتدا باید پیش‌نیازهای این درس را بگذرانید: "
                    + "، ".join(missing_courses)
                )

            # بررسی ظرفیت
            enrolled_count = Enrollment.objects.filter(
                class_section=section,
                status="ENROLLED",
            ).count()

            if enrolled_count >= section.capacity:
                return error("ظرفیت این گروه تکمیل شده است.")

            # بررسی تداخل برنامه هفتگی
            selected_schedules = list(
                ClassSchedule.objects.filter(
                    class_section=section,
                )
            )

            for enrollment in current_enrollments:
                existing_schedules = ClassSchedule.objects.filter(
                    class_section=enrollment.class_section,
                )

                for new_schedule in selected_schedules:
                    for old_schedule in existing_schedules:
                        same_day = (
                                new_schedule.day_of_week
                                == old_schedule.day_of_week
                        )

                        overlaps = (
                                new_schedule.start_time < old_schedule.end_time
                                and new_schedule.end_time > old_schedule.start_time
                        )

                        if same_day and overlaps:
                            return error(
                                "زمان این کلاس با یکی از درس‌های "
                                "انتخاب‌شده تداخل دارد."
                            )

            # ثبت نهایی در دیتابیس
            Enrollment.objects.create(
                student=student,
                class_section=section,
                status="ENROLLED",
                registered_at=now,
                dropped_at=None,
            )

        return Response(
            {
                "success": True,
                "message": "انتخاب واحد با موفقیت انجام شد.",
                "class_section_id": section.pk,
                "course_title": course.title,
                "section_code": section.section_code,
                "professor_name": professor_name,
            },
            status=status.HTTP_201_CREATED,
        )


class DropEnrollmentView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, class_section_id):
        now = timezone.now()

        with transaction.atomic():
            try:
                student = (
                    Student.objects
                    .select_for_update()
                    .get(person=request.user.person)
                )
            except (Student.DoesNotExist, AttributeError):
                return Response(
                    {
                        "success": False,
                        "message": "پروفایل دانشجویی پیدا نشد.",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            # فقط در بازه فعال انتخاب واحد امکان لغو وجود دارد.
            active_period = EnrollmentPeriod.objects.filter(
                is_open=True,
                start_at__lte=now,
                end_at__gte=now,
                semester__is_active=True,
            ).first()

            if active_period is None:
                return Response(
                    {
                        "success": False,
                        "message": "در حال حاضر امکان لغو انتخاب واحد وجود ندارد.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            enrollment = (
                Enrollment.objects
                .select_for_update()
                .filter(
                    student=student,
                    class_section_id=class_section_id,
                    class_section__course_offering__semester_id=(
                        active_period.semester_id
                    ),
                )
                .first()
            )

            if enrollment is None:
                return Response(
                    {
                        "success": False,
                        "message": "ثبت‌نام این درس برای شما پیدا نشد.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            if enrollment.status != "ENROLLED":
                return Response(
                    {
                        "success": False,
                        "message": "این درس قبلاً لغو شده است.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            enrollment.status = "DROPPED"
            enrollment.dropped_at = now
            enrollment.save(
                update_fields=["status", "dropped_at"]
            )

        return Response(
            {
                "success": True,
                "message": "درس با موفقیت از دروس انتخاب شده حذف شد.",
                "class_section_id": class_section_id,
            },
            status=status.HTTP_200_OK,
        )


class MyEnrollmentsView(APIView):
    """
    فهرست درس‌های ثبت‌شده دانشجو در نیمسال فعال،
    همراه با برنامه هفتگی، استاد و محل برگزاری.
    """

    permission_classes = [IsAuthenticated, IsStudent]

    @extend_schema(responses={200: dict})
    def get(self, request):
        student = get_student_for_user(request.user)

        if student is None:
            return Response(
                {
                    "success": False,
                    "message": "پروفایل دانشجویی پیدا نشد.",
                    "results": [],
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        now = timezone.now()

        active_period = (
            EnrollmentPeriod.objects
            .filter(
                is_open=True,
                start_at__lte=now,
                end_at__gte=now,
                semester__is_active=True,
            )
            .select_related("semester")
            .order_by("-start_at")
            .first()
        )

        enrollments = (
            Enrollment.objects
            .filter(
                student=student,
                status="ENROLLED",
            )
            .select_related(
                "class_section",
                "class_section__professor",
                "class_section__professor__person",
                "class_section__course_offering",
                "class_section__course_offering__course",
                "class_section__course_offering__semester",
            )
            .prefetch_related(
                "class_section__schedules__room__building",
            )
            .order_by("-registered_at")
        )

        # در صورت وجود نیمسال فعال، فقط درس‌های همان نیمسال نمایش داده می‌شوند.
        if active_period is not None:
            enrollments = enrollments.filter(
                class_section__course_offering__semester=(
                    active_period.semester
                )
            )

        results = []

        for enrollment in enrollments:
            section = enrollment.class_section
            offering = section.course_offering
            course = offering.course
            professor = section.professor

            # نام استاد از مدل Person دریافت می‌شود.
            professor_name = ""

            if professor and professor.person:
                professor_name = (
                    f"{professor.person.first_name or ''} "
                    f"{professor.person.last_name or ''}"
                ).strip()

            schedules = []

            for schedule in section.schedules.all():
                room = schedule.room
                building = room.building if room else None

                room_number = room.room_number if room else ""
                building_name = building.name if building else ""

                if building_name and room_number:
                    location = (
                        f"{building_name}، اتاق {room_number}"
                    )
                elif room_number:
                    location = f"اتاق {room_number}"
                elif building_name:
                    location = building_name
                else:
                    location = "محل کلاس ثبت نشده"

                schedules.append(
                    {
                        "day_of_week": schedule.day_of_week,
                        "start_time": (
                            schedule.start_time.strftime("%H:%M")
                            if schedule.start_time
                            else None
                        ),
                        "end_time": (
                            schedule.end_time.strftime("%H:%M")
                            if schedule.end_time
                            else None
                        ),
                        "room_number": room_number,
                        "building": building_name,
                        "room_type": (
                            room.room_type if room else ""
                        ),
                        "location": location,
                    }
                )

            results.append(
                {
                    "id": section.pk,
                    "class_section_id": section.pk,
                    "section_code": section.section_code,
                    "course_title": course.title,
                    "course_code": course.course_code,
                    "units": course.units,
                    "course_type": course.course_type,
                    "semester": offering.semester.title,
                    "professor_name": professor_name,
                    "status": enrollment.status,
                    "registered_at": enrollment.registered_at,
                    "schedules": schedules,
                }
            )

        return Response(
            {
                "success": True,
                "semester": (
                    active_period.semester.title
                    if active_period
                    else None
                ),
                "results": results,
            },
            status=status.HTTP_200_OK,
        )
