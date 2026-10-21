
from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    allowed_roles = ()

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if not user.is_active or user.is_locked:
            return False

        return user.user_roles.filter(
            role__name__in=self.allowed_roles,
            role__is_active=True,
        ).exists()


class IsStudent(HasRole):
    allowed_roles = ("STUDENT",)


class IsProfessor(HasRole):
    allowed_roles = ("PROFESSOR",)


class IsStaff(HasRole):
    allowed_roles = ("STAFF",)


class IsAdmin(HasRole):
    allowed_roles = ("ADMIN",)