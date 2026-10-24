
from django.urls import path

from .views import StudentGradesView

urlpatterns = [
    path(
        "student/grades/",
        StudentGradesView.as_view(),
        name="student-grades",
    ),
]
