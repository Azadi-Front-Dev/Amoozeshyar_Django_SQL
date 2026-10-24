
from rest_framework import serializers


class AvailableCourseSerializer(serializers.Serializer):
    class_section_id = serializers.IntegerField()
    section_code = serializers.CharField()

    course_code = serializers.IntegerField(
        source="course_offering.course.course_code"
    )
    course_title = serializers.CharField(
        source="course_offering.course.title"
    )
    units = serializers.IntegerField(
        source="course_offering.course.units"
    )
    semester_title = serializers.CharField(
        source="course_offering.semester.title"
    )

    capacity = serializers.SerializerMethodField()
    enrolled_count = serializers.IntegerField()
    remaining_capacity = serializers.SerializerMethodField()
    schedules = serializers.SerializerMethodField()

    def get_capacity(self, obj):
        return obj.capacity

    def get_remaining_capacity(self, obj):
        return max(obj.capacity - obj.enrolled_count, 0)


    def get_schedules(self, obj):
        schedules = obj.schedules.all()

        return [
            {
                "day_of_week": schedule.day_of_week,
                "start_time": schedule.start_time,
                "end_time": schedule.end_time,
            }
            for schedule in schedules
        ]



class EnrollRequestSerializer(serializers.Serializer):
    class_section_id = serializers.IntegerField()
