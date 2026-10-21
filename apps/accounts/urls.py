from django.urls import path
from .views import RegisterView, LoginView, MeView, StudentDashboardView
from .views import (
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", MeView.as_view(), name="me"),
    path(
        "student/dashboard/",
        StudentDashboardView.as_view(),
        name="student-dashboard",
    ),
    path(
        "password-reset/request/",
        PasswordResetRequestView.as_view(),
        name="password-reset-request",
    ),
    path(
        "password-reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "student/dashboard/",
        StudentDashboardView.as_view(),
        name="student-dashboard",
    ),
]
