
from django.urls import path

from apps.academic.views import (
    UniversityDetailView,
    UniversityListView,
)

app_name = "academic"

urlpatterns = [
    path(
        "universities/",
        UniversityListView.as_view(),
        name="university-list",
    ),
    path(
        "universities/<int:university_id>/",
        UniversityDetailView.as_view(),
        name="university-detail",
    ),
]