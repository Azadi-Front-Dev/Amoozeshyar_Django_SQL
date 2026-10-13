
from django.db.models import Q, QuerySet
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import OpenApiParameter, extend_schema

from apps.academic.models import (
    University,
    Faculty,
    Department,
    EducationLevel,
    FieldOfStudy,
)
from apps.academic.serializers import (
    UniversitySerializer,
    UniversityQuerySerializer,
    FacultySerializer,
    DepartmentSerializer,
    EducationLevelSerializer,
    FieldOfStudySerializer,
    AcademicQuerySerializer,
)


class AcademicPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class UniversityPagination(AcademicPagination):
    pass


class UniversityQueryMixin:
    def get_queryset(self) -> QuerySet:
        params = UniversityQuerySerializer(
            data=self.request.query_params,
        )
        params.is_valid(raise_exception=True)
        filters = params.validated_data

        queryset = University.objects.all()

        if "is_active" in filters:
            queryset = queryset.filter(
                is_active=filters["is_active"],
            )

        search = filters.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(code__icontains=search)
            )

        return queryset.order_by(filters.get("ordering", "name"))


class AcademicQueryMixin:
    query_serializer_class = AcademicQuerySerializer

    def get_queryset(self) -> QuerySet:
        params = self.query_serializer_class(
            data=self.request.query_params,
        )
        params.is_valid(raise_exception=True)
        filters = params.validated_data

        queryset = self.model.objects.all()

        if "is_active" in filters and hasattr(self.model, "is_active"):
            queryset = queryset.filter(
                is_active=filters["is_active"],
            )

        search = filters.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(code__icontains=search)
            )

        for field in (
            "university",
            "faculty",
            "department",
            "education_level",
        ):
            if field in filters:
                if field == "university" and self.model is Faculty:
                    queryset = queryset.filter(
                        university_id=filters[field],
                    )
                elif field == "university" and self.model is Department:
                    queryset = queryset.filter(
                        faculty__university_id=filters[field],
                    )
                elif field == "university" and self.model is FieldOfStudy:
                    queryset = queryset.filter(
                        department__faculty__university_id=filters[field],
                    )
                elif field == "faculty" and self.model is Department:
                    queryset = queryset.filter(
                        faculty_id=filters[field],
                    )
                elif field == "faculty" and self.model is FieldOfStudy:
                    queryset = queryset.filter(
                        department__faculty_id=filters[field],
                    )
                elif field == "department" and self.model is FieldOfStudy:
                    queryset = queryset.filter(
                        department_id=filters[field],
                    )
                elif field == "education_level" and self.model is FieldOfStudy:
                    queryset = queryset.filter(
                        education_level_id=filters[field],
                    )

        ordering = filters.get("ordering", "name")
        return queryset.order_by(ordering)


class UniversityListView(
    UniversityQueryMixin,
    generics.ListAPIView,
):
    serializer_class = UniversitySerializer
    pagination_class = UniversityPagination


class UniversityDetailView(generics.RetrieveAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    lookup_field = "university_id"
    lookup_url_kwarg = "university_id"


@extend_schema(tags=["Academic - Faculties"])
class FacultyListView(AcademicQueryMixin, generics.ListAPIView):
    model = Faculty
    serializer_class = FacultySerializer
    pagination_class = AcademicPagination

    def get_queryset(self):
        return super().get_queryset().select_related("university")


class FacultyDetailView(generics.RetrieveAPIView):
    queryset = Faculty.objects.select_related("university")
    serializer_class = FacultySerializer
    lookup_field = "faculty_id"
    lookup_url_kwarg = "faculty_id"


@extend_schema(tags=["Academic - Departments"])
class DepartmentListView(AcademicQueryMixin, generics.ListAPIView):
    model = Department
    serializer_class = DepartmentSerializer
    pagination_class = AcademicPagination

    def get_queryset(self):
        return super().get_queryset().select_related(
            "faculty",
            "faculty__university",
        )


class DepartmentDetailView(generics.RetrieveAPIView):
    queryset = Department.objects.select_related(
        "faculty",
        "faculty__university",
    )
    serializer_class = DepartmentSerializer
    lookup_field = "department_id"
    lookup_url_kwarg = "department_id"


@extend_schema(tags=["Academic - Education Levels"])
class EducationLevelListView(
    AcademicQueryMixin,
    generics.ListAPIView,
):
    model = EducationLevel
    serializer_class = EducationLevelSerializer
    pagination_class = AcademicPagination


class EducationLevelDetailView(generics.RetrieveAPIView):
    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer
    lookup_field = "education_level_id"
    lookup_url_kwarg = "education_level_id"


@extend_schema(tags=["Academic - Fields of Study"])
class FieldOfStudyListView(
    AcademicQueryMixin,
    generics.ListAPIView,
):
    model = FieldOfStudy
    serializer_class = FieldOfStudySerializer
    pagination_class = AcademicPagination

    def get_queryset(self):
        return super().get_queryset().select_related(
            "department",
            "department__faculty",
            "department__faculty__university",
            "education_level",
        )


class FieldOfStudyDetailView(generics.RetrieveAPIView):
    queryset = FieldOfStudy.objects.select_related(
        "department",
        "department__faculty",
        "department__faculty__university",
        "education_level",
    )
    serializer_class = FieldOfStudySerializer
    lookup_field = "field_of_study_id"
    lookup_url_kwarg = "field_of_study_id"
