from rest_framework import serializers
from .models import StudentAttendance, GuestAttendance
from students.models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "name", "roll_no"]  # Include roll_no

class StudentAttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)  # Nested serializer

    class Meta:
        model = StudentAttendance
        fields = ["id", "student", "photo", "marked_at"]  # student now includes name + roll_no

class GuestAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestAttendance
        fields = ["id", "image", "marked_at"]
