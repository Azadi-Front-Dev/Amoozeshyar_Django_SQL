
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import Person

from .models import UserAccount
from .serializers import LoginSerializer, RegisterSerializer
from .services import authenticate_account


class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        now = timezone.now()

        with transaction.atomic():
            person = Person.objects.create(
                national_id=data["national_id"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                is_active=True,
                created_at=now,
            )

            account = UserAccount.objects.create(
                person=person,
                username=data["username"],
                password_hash=make_password(data["password"]),
                is_active=True,
                is_locked=False,
                created_at=now,
            )

        return Response(
            {
                "message": "Account created successfully.",
                "user": {
                    "id": account.user_id,
                    "username": account.username,
                    "first_name": person.first_name,
                    "last_name": person.last_name,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = authenticate_account(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if account is None:
            return Response(
                {"detail": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken()
        refresh["user_id"] = account.user_id

        roles = list(
            account.user_roles.filter(role__is_active=True)
            .values_list("role__name", flat=True)
        )

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": account.user_id,
                    "username": account.username,
                    "first_name": account.person.first_name,
                    "last_name": account.person.last_name,
                    "roles": roles,
                },
            },
            status=status.HTTP_200_OK,
        )


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account = request.user

        roles = list(
            account.user_roles.filter(role__is_active=True)
            .values_list("role__name", flat=True)
        )

        return Response(
            {
                "id": account.user_id,
                "username": account.username,
                "first_name": account.person.first_name,
                "last_name": account.person.last_name,
                "roles": roles,
            },
            status=status.HTTP_200_OK,
        )
