
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=50,
        trim_whitespace=True,
    )
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )


class RegisterSerializer(serializers.Serializer):
    national_id = serializers.RegexField(r"^\d{10}$")
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    phone_number = serializers.RegexField(r"^\+?[0-9]{10,15}$")
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(
        min_length=8,
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )

    def validate_national_id(self, value):
        from apps.users.models import Person

        if Person.objects.filter(national_id=value).exists():
            raise serializers.ValidationError(
                "This national ID is already registered."
            )
        return value

    def validate_phone_number(self, value):
        from apps.users.models import Person

        if Person.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "This phone number is already registered."
            )
        return value

    def validate_username(self, value):
        from apps.accounts.models import UserAccount

        if UserAccount.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "This username is already taken."
            )
        return value
