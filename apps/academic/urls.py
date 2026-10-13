
from django.urls import path

from apps.academic.views import (
    UniversityListView,
    UniversityDetailView,
    FacultyListView,
    FacultyDetailView,
    DepartmentListView,
    DepartmentDetailView,
    EducationLevelListView,
    EducationLevelDetailView,
    FieldOfStudyListView,
    FieldOfStudyDetailView,
)

app_name = "academic"

urlpatterns = [
    path("universities/", UniversityListView.as_view(), name="university-list"),
    path("universities/<int:university_id>/", UniversityDetailView.as_view(), name="university-detail"),

    path("faculties/", FacultyListView.as_view(), name="faculty-list"),
    path("faculties/<int:faculty_id>/", FacultyDetailView.as_view(), name="faculty-detail"),

    path("departments/", DepartmentListView.as_view(), name="department-list"),
    path("departments/<int:department_id>/", DepartmentDetailView.as_view(), name="department-detail"),

    path("education-levels/", EducationLevelListView.as_view(), name="education-level-list"),
    path("education-levels/<int:education_level_id>/", EducationLevelDetailView.as_view(), name="education-level-detail"),

    path("fields-of-study/", FieldOfStudyListView.as_view(), name="field-of-study-list"),
    path("fields-of-study/<int:field_of_study_id>/", FieldOfStudyDetailView.as_view(), name="field-of-study-detail"),
]
