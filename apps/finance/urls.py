
from django.urls import path

from .views import StudentFinanceView

urlpatterns = [
    path(
        "student/",
        StudentFinanceView.as_view(),
        name="student-finance",
    ),
]
