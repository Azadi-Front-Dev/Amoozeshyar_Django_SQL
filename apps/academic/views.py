
from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
)

from apps.academic.models import University
from apps.academic.serializers import (
    UniversityQuerySerializer,
    UniversitySerializer,
)


class UniversityPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


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
            from django.db.models import Q

            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(code__icontains=search)
            )

        ordering = filters.get("ordering", "name")
        return queryset.order_by(ordering)


@extend_schema(
    tags=["Academic - Universities"],
    summary="List universities",
    description=(
        "Retrieve a paginated list of universities. "
        "Supports filtering by active status, searching by "
        "name or code, and ordering."
    ),
    parameters=[
        OpenApiParameter(
            name="is_active",
            type=bool,
            location=OpenApiParameter.QUERY,
            description="Filter by active status: true or false.",
        ),
        OpenApiParameter(
            name="search",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Search by university name or code.",
        ),
        OpenApiParameter(
            name="ordering",
            type=str,
            location=OpenApiParameter.QUERY,
            enum=[
                "university_id",
                "-university_id",
                "name",
                "-name",
                "code",
                "-code",
                "created_at",
                "-created_at",
            ],
            description="Field used to order the results. Prefix with - for descending order.",
        ),
        OpenApiParameter(
            name="page",
            type=int,
            location=OpenApiParameter.QUERY,
            description="Page number; starts at 1.",
        ),
        OpenApiParameter(
            name="page_size",
            type=int,
            location=OpenApiParameter.QUERY,
            description="Number of results per page; maximum 100.",
        ),
    ],
)
class UniversityListView(
    UniversityQueryMixin,
    generics.ListAPIView,
):
    serializer_class = UniversitySerializer
    pagination_class = UniversityPagination


@extend_schema(
    tags=["Academic - Universities"],
    summary="Retrieve university details",
    description="Retrieve one university using its ID.",
)
class UniversityDetailView(generics.RetrieveAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    lookup_field = "university_id"
    lookup_url_kwarg = "university_id"