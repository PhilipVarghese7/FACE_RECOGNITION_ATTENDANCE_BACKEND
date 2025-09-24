from rest_framework import serializers
from .models import StudentAttendance,GuestAttendance

class StudentAttendanceSerializer(serializers.ModelSerializer):
    student_name=serializers.CharField(source="student.name",read_only=True)
    class Meta:
        model=StudentAttendance
        fields=["id","student","student_name","photo","marked_at"]


class GuestAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=GuestAttendance
        fields=["id","image","marked_at"]