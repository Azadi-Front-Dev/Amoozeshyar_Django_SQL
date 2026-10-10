
from rest_framework import serializers

from apps.academic.models import University


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = (
            "university_id",
            "name",
            "code",
            "is_active",
            "created_at",
        )
        read_only_fields = fields


class UniversityQuerySerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=False)

    search = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=200,
    )

    ordering = serializers.ChoiceField(
        required=False,
        choices=(
            "university_id",
            "-university_id",
            "name",
            "-name",
            "code",
            "-code",
            "created_at",
            "-created_at",
        ),
    )