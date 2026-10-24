from django.urls import path

from apps.registration.views import (
    AvailableCoursesView,
    EnrollStudentView,
    MyEnrollmentsView,
)
from apps.registration.views import DropEnrollmentView

urlpatterns = [
    path(
        "student/available-courses/",
        AvailableCoursesView.as_view(),
        name="available-courses",
    ),
    path(
        "student/enroll/",
        EnrollStudentView.as_view(),
        name="enroll-student",
    ),
    path(
        "student/my-enrollments/",
        MyEnrollmentsView.as_view(),
        name="my-enrollments",
    ),
    path(
        "student/enroll/<int:class_section_id>/drop/",
        DropEnrollmentView.as_view(),
        name="drop-enrollment",
    ),

]
