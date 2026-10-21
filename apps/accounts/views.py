import secrets
from hashlib import sha256

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import Person, Student
from apps.accounts.permissions import IsStudent
from apps.education.models import Semester, ClassSchedule
from apps.registration.models import Enrollment

from .models import UserAccount
from .serializers import LoginSerializer, RegisterSerializer
from .services import authenticate_account


class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        now = timezone.now()

        with transaction.atomic():
            person = Person.objects.create(
                national_id=data["national_id"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                is_active=True,
                created_at=now,
            )

            account = UserAccount.objects.create(
                person=person,
                username=data["username"],
                password_hash=make_password(data["password"]),
                is_active=True,
                is_locked=False,
                created_at=now,
            )

        return Response(
            {
                "message": "Account created successfully.",
                "user": {
                    "id": account.user_id,
                    "username": account.username,
                    "first_name": person.first_name,
                    "last_name": person.last_name,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = authenticate_account(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if account is None:
            return Response(
                {"detail": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken()
        refresh["user_id"] = account.user_id

        roles = list(
            account.user_roles.filter(role__is_active=True)
            .values_list("role__name", flat=True)
        )

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": account.user_id,
                    "username": account.username,
                    "first_name": account.person.first_name,
                    "last_name": account.person.last_name,
                    "roles": roles,
                },
            },
            status=status.HTTP_200_OK,
        )


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account = request.user

        roles = list(
            account.user_roles.filter(role__is_active=True)
            .values_list("role__name", flat=True)
        )

        return Response(
            {
                "id": account.user_id,
                "username": account.username,
                "first_name": account.person.first_name,
                "last_name": account.person.last_name,
                "roles": roles,
            },
            status=status.HTTP_200_OK,
        )


class StudentDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        account = request.user
        person = account.person

        # دریافت اطلاعات دانشجو
        try:
            student = Student.objects.get(person=person)
        except Student.DoesNotExist:
            return Response(
                {"detail": "اطلاعات دانشجو پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # دریافت ترم فعال
        semester = (
            Semester.objects
            .filter(
                is_active=True,
                academic_year__is_active=True,
            )
            .select_related("academic_year")
            .first()
        )

        # اطلاعات شخصی
        person_data = {
            "first_name": person.first_name,
            "last_name": person.last_name,
            "national_id": person.national_id,
            "phone_number": person.phone_number,
            "email": person.email,
        }

        # اطلاعات حساب کاربری
        user_data = {
            "username": account.username,
        }

        # اطلاعات تحصیلی دانشجو
        student_data = {
            "student_number": student.student_number,
            "entry_year": student.entry_year,
            "status": student.status,
            "field_of_study": (
                str(student.field_of_study)
                if student.field_of_study
                else None
            ),
        }

        # اگر ترم فعالی وجود نداشته باشد
        if semester is None:
            return Response(
                {
                    "user": user_data,
                    "person": person_data,
                    "student": student_data,
                    "semester": None,
                    "summary": {
                        "course_count": 0,
                        "total_units": 0,
                    },
                    "courses": [],
                    "schedule": [],
                },
                status=status.HTTP_200_OK,
            )

        # دریافت درس‌های ثبت‌نام‌شده دانشجو در ترم فعال
        enrollments = (
            Enrollment.objects
            .filter(
                student=student,
                class_section__course_offering__semester=semester,
                dropped_at__isnull=True,
                status="ENROLLED",
            )
            .select_related(
                "class_section__course_offering__course",
                "class_section__professor__person",
            )
            .prefetch_related(
                "class_section__schedules__room__building"
            )
        )

        courses = []
        schedule = []
        total_units = 0

        # آماده‌سازی اطلاعات درس‌ها و برنامه هفتگی
        for enrollment in enrollments:
            section = enrollment.class_section
            course = section.course_offering.course
            professor = section.professor

            # نام استاد؛ در صورت نداشتن استاد مقدار مشخصی برگردانده می‌شود
            professor_name = None
            if professor is not None and professor.person is not None:
                professor_name = (
                    f"{professor.person.first_name} "
                    f"{professor.person.last_name}"
                )

            courses.append({
                "enrollment_id": enrollment.enrollment_id,
                "course_code": course.course_code,
                "course_title": course.title,
                "units": course.units,
                "section_code": section.section_code,
                "professor": professor_name,
            })

            total_units += course.units or 0

            # برنامه زمانی کلاس‌ها
            for item in section.schedules.all():
                room = item.room
                building = room.building if room is not None else None

                schedule.append({
                    "course_title": course.title,
                    "day_of_week": item.day_of_week,
                    "start_time": (
                        item.start_time.strftime("%H:%M")
                        if item.start_time is not None
                        else None
                    ),
                    "end_time": (
                        item.end_time.strftime("%H:%M")
                        if item.end_time is not None
                        else None
                    ),
                    "building": (
                        building.name
                        if building is not None
                        else None
                    ),
                    "room_number": (
                        room.room_number
                        if room is not None
                        else None
                    ),
                })

        # مرتب‌سازی برنامه بر اساس روز و ساعت شروع
        schedule.sort(
            key=lambda item: (
                item["day_of_week"] or 0,
                item["start_time"] or "",
            )
        )

        # پاسخ نهایی داشبورد
        return Response(
            {
                "user": user_data,
                "person": person_data,
                "student": student_data,
                "semester": {
                    "title": semester.title,
                    "academic_year": (
                        semester.academic_year.title
                        if semester.academic_year is not None
                        else None
                    ),
                    "start_date": semester.start_date,
                    "end_date": semester.end_date,
                },
                "summary": {
                    "course_count": len(courses),
                    "total_units": total_units,
                },
                "courses": courses,
                "schedule": schedule,
            },
            status=status.HTTP_200_OK,
        )





# -------
# class StudentDashboardView(APIView):
#     permission_classes = [IsAuthenticated, IsStudent]
#
#     def get(self, request):
#         account = request.user
#         person = account.person
#
#         try:
#             student = person.student
#         except person.student.RelatedObjectDoesNotExist:
#             student = None
#
#         student_info = None
#
#         if student:
#             student_info = {
#                 "student_number": student.student_number,
#                 "entry_year": student.entry_year,
#                 "status": student.status,
#                 "field_of_study": (
#                     str(student.field_of_study)
#                     if student.field_of_study
#                     else None
#                 ),
#             }
#
#         return Response({
#             "user": {
#                 "username": account.username,
#             },
#             "person": {
#                 "first_name": person.first_name,
#                 "last_name": person.last_name,
#                 "national_id": person.national_id,
#                 "phone_number": person.phone_number,
#                 "email": person.email,
#             },
#             "student": student_info,
#         })

# ---------------------- بازیابی رمز عبور

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        national_id = str(request.data.get("national_id", "")).strip()
        phone_number = str(request.data.get("phone_number", "")).strip()

        if not national_id or not phone_number:
            return Response(
                {"detail": "کد ملی و شماره تلفن الزامی است."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # محدودسازی درخواست‌های مکرر برای این ورودی
        from hashlib import sha256

        request_key = "otp_request:" + sha256(
            f"{national_id}:{phone_number}".encode()
        ).hexdigest()

        if not cache.add(request_key, True, timeout=60):
            return Response(
                {"detail": "لطفاً کمی بعد دوباره تلاش کنید."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        account = UserAccount.objects.filter(
            person__national_id=national_id,
            person__phone_number=phone_number,
            person__is_active=True,
            is_active=True,
            is_locked=False,
        ).first()

        # پیام عمومی، برای جلوگیری از افشای وجود حساب
        if account is None:
            return Response({
                "detail": "اگر اطلاعات معتبر باشد، کد بازیابی صادر می‌شود."
            })

        otp = f"{secrets.randbelow(1_000_000):06d}"

        cache.set(
            f"password_reset_otp:{account.user_id}",
            {
                "otp_hash": make_password(otp),
                "attempts": 0,
            },
            timeout=300,
        )

        # فقط برای توسعه محلی؛ در محیط واقعی حذف شود
        print(f"[DEV OTP] UserId={account.user_id} OTP={otp}")

        return Response({
            "detail": "اگر اطلاعات معتبر باشد، کد بازیابی صادر می‌شود."
        })


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        national_id = str(request.data.get("national_id", "")).strip()
        phone_number = str(request.data.get("phone_number", "")).strip()
        otp = str(request.data.get("otp", "")).strip()
        new_password = request.data.get("new_password", "")

        if not all([national_id, phone_number, otp, new_password]):
            return Response(
                {"detail": "تمام فیلدها الزامی هستند."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(new_password) < 8:
            return Response(
                {"detail": "رمز عبور باید حداقل ۸ کاراکتر باشد."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        account = UserAccount.objects.filter(
            person__national_id=national_id,
            person__phone_number=phone_number,
            person__is_active=True,
            is_active=True,
            is_locked=False,
        ).first()

        if account is None:
            return Response(
                {"detail": "کد یا اطلاعات واردشده معتبر نیست."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cache_key = f"password_reset_otp:{account.user_id}"
        otp_data = cache.get(cache_key)

        if otp_data is None:
            return Response(
                {"detail": "کد منقضی شده است؛ دوباره درخواست کد بدهید."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if otp_data["attempts"] >= 5:
            cache.delete(cache_key)
            return Response(
                {"detail": "تعداد تلاش‌ها بیش از حد مجاز است."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(otp) != 6 or not otp.isdigit() or not check_password(
                otp, otp_data["otp_hash"]
        ):
            otp_data["attempts"] += 1
            cache.set(cache_key, otp_data, timeout=300)

            return Response(
                {"detail": "کد تأیید نادرست است."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ذخیره رمز جدید به‌صورت هش
        account.password_hash = make_password(new_password)
        account.save(update_fields=["password_hash"])

        # کد پس از استفاده حذف می‌شود
        cache.delete(cache_key)

        return Response({
            "detail": "رمز عبور با موفقیت تغییر کرد."
        })
