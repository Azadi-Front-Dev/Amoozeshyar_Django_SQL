
from django.db.models import Prefetch

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsStudent
from apps.registration.models import Enrollment
from .models import ExamResult
from .serializers import StudentGradeSerializer


class StudentGradesView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        enrollments = (
            Enrollment.objects
            .filter(student__person=request.user.person)
            .select_related(
                "class_section__course_offering__course",
                "class_section__course_offering__semester__academic_year",
            )
            .prefetch_related(
                "course_grade",
                Prefetch(
                    "exam_results",
                    queryset=ExamResult.objects
                    .select_related("exam")
                    .order_by("exam__exam_date"),
                ),
            )
            .order_by("-registered_at")
        )

        data = StudentGradeSerializer(
            enrollments,
            many=True,
        ).data

        return Response({
            "count": len(data),
            "results": data,
        })
